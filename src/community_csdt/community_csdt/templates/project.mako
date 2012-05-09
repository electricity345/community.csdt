<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Project | ${proj_name}</title>
</%block>

<%block name="scripts">
  $(function(){			
    stars_choice_obj = $("#stars-choice").stars({
      inputType: "select",
      captionEl: $("#stars-choice-cap"),
      <%
        if "username" in session and session["username"] == owner:
          context.write("disabled: true,")
      %>
      callback: function(ui, type, value) {
        <%
          if "username" not in session:
            context.write("location.href=\"/login\";")
            context.write("return false;")
        %>
        $.ajax({
          type: "POST",
          url: "/projects/submit-rating?proj_id=${proj_id}",
          data: {
            rating : value
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);

            initializeAverageStars(stars_choice_obj);
            return;
          },
          error: function(jqXHR, textStatus, errorThrown) {
            alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
            location.href = "/";
          }
        });
      }
    }).data("stars");

    function initializeAverageStars(stars_choice_obj) {
      $.ajax({
        type: "POST",
        url: "/projects/average-ratings?proj_id=${proj_id}",
        success: function(result) {
          var obj = jQuery.parseJSON(result);
  
          $("#stars-average-cap").text("+ " + obj.num_reviews + " from (" + obj.num_reviews + " votes)");
          $("#stars-average-off").width(stars_choice_obj.options.starWidth * stars_choice_obj.options.items);
          $("#stars-average-on").width(Math.round( $("#stars-average-off").width() / stars_choice_obj.options.items * parseFloat(obj.avg_rating) ));
          return;
        },
        error: function(jqXHR, textStatus, errorThrown) {
          alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
          location.href = "/";
        }
      });
      return;
    }

    function initializeRatingStars() {
      $.ajax({
        type: "POST",
        url: "/projects/user-rating?proj_id=${proj_id}",
        success: function(result) {
          var obj = jQuery.parseJSON(result);
          
          $("#stars-choice").stars("select", obj.rating);
          return;
        },
        error: function(jqXHR, textStatus, errorThrown) {
          alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
          location.href = "/";
        }
      });
      return;
    }

    initializeAverageStars(stars_choice_obj);
    <%
      if "username" in session:
        context.write("initializeRatingStars();")
    %>

    $("#checklength-false").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#project-description-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#add-comment-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#comment-flag-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });
    
    $("#comment-flag-failure").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          $(this).dialog("close"); 
        }
      }
    });
    
    $("#comment-rating-failure-1").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          $(this).dialog("close"); 
        }
      }
    });

    $("#comment-rating-failure-2").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          $(this).dialog("close"); 
        }
      }
    });

    $("#comment-rating-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    function checkDescriptionLength() {
      var description = $("textarea#description").val();
      
      if (description.length > 200) {
        return false;
      }

      return true;
    }

    $("#project-description").validate({
      rules: {
        description: {
          maxlength: 200
        }
      },
      messages: {
        description: {
          maxlength: "Your project description must be no more than 200 characters long"
        }
      }
    });

    function checkBodyLength() {
      var body = $("textarea#body").val();
      
      if (body.length > 200) {
        return false;
      }

      return true;
    }

    $("#add-comment").validate({
      rules: {
        body: {
          maxlength: 200
        }
      },
      messages: {
        body: {
          maxlength: "Your comment must be no more than 200 characters long"
        }
      }
    });

    $("#project-description-save").click(function(){
      $("#project-description").submit(function() {
        if (checkDescriptionLength() == false) {
          $("#checklength-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "${path_url}/description-edit-forms?proj_id=${proj_id}",
          data: {
            description : $("textarea#description").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              $("#project-description-success").dialog("open");
            } 
          },
          error: function(jqXHR, textStatus, errorThrown) {
            alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
            location.href = "/";
          }
        });
        return false;
      });
    });

    $("#comment-submit").click(function(){
      <%
        if "username" not in session:
          context.write("$(\"#login-form\").dialog(\"open\");")
          context.write("return false;")
      %>

      $("#add-comment").submit(function() {
        if (checkBodyLength() == false) {
          $("#checklength-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "${path_url}/comments/add?proj_id=${proj_id}",
          data: {
            body : $("textarea#body").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              $("#add-comment-success").dialog("open");
            } 
          },
          error: function(jqXHR, textStatus, errorThrown) {
            alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
            location.href = "/";
          }
        });
        return false;
      });
    });

    function getAllComments() {
      $.ajax({
        type: "POST",
        url: "${path_url}/comments/all?proj_id=${proj_id}",
        success: function(result) {
          var obj = jQuery.parseJSON(result);
          result = obj.result;
          for (var i = 0; i < obj.dict_length; i++) {
            content = "";
            if (parseInt(result[i]["flag"]) > 0) {
              content = "<div class=\"comment\"> <div class=\"avatar\"> <img src=/static/css/comment/img/default_avatar.gif /> </div> <div class=\"name\"><a href=\"/accounts/" + result[i]["username"] + "\">" + result[i]["username"] + "</a></div> <div class=\"date\" title=\"Added\">" + result[i]["time"] + "</div> <p><i>This comment has been flagged</i><a href=\"#\" id=\"comment-" + i + "-show\" class=\"display-data\" onclick=\"showHideContent(\'comment-" + i + "\');return false;\">Show</a></p> <div id=\"comment-" + i + "\" class=\"more-data\"><p>" + result[i]["text"] + "</p> <p><a href=\"#\" class=\"mask-data\" onclick=\"showHideContent(\'comment-" + i + "\');return false;\">Hide</a></p></div><div class=\"bottom\"><span><a href=\"javascript:void(0);\" onclick=\"flagComment(" + result[i]["id"] + ");\">Flag</a></span><span><a href=\"javascript:void(0);\" onclick=\"submitCommentRating(" + result[i]["id"] + ",1);\">Likes(" + result[i]["ratings"] +")</a></span><a href=\"#\">Reply</a></div></div>";
            } else {
              content = "<div class=\"comment\"> <div class=\"avatar\"> <img src=/static/css/comment/img/default_avatar.gif /> </div> <div class=\"name\"><a href=\"/accounts/" + result[i]["username"] + "\">" + result[i]["username"] + "</a></div> <div class=\"date\" title=\"Added\">" + result[i]["time"] + "</div> <p>" + result[i]["text"] + "</p> <div class=\"bottom\"><span><a href=\"javascript:void(0);\" onclick=\"flagComment(" + result[i]["id"] + ");\">Flag</a></span><span><a href=\"javascript:void(0);\" onclick=\"submitCommentRating(" + result[i]["id"] + ",1);\">Likes(" + result[i]["ratings"] +")</a></span><a href=\"#\">Reply</a></div></div>";
            }
            $(content).appendTo("#all-comment-posts");
          }
          
          return;
        },
        error: function(jqXHR, textStatus, errorThrown) {
          alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
          location.href = "/";
        }
      });
      return;
    }

    getAllComments();
  });

  function flagComment(comment_id) {
    $.ajax({
      type: "POST",
      url: "${path_url}/comments/flag?proj_id=${proj_id}",
      data: {
        comment_id: comment_id
      },
      success: function(result) {
        var obj = jQuery.parseJSON(result);
        if (obj.result == -1) {
          $("#comment-flag-failure").dialog("open");  
        } else {
          $("#comment-flag-success").dialog("open");
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
        location.href = "/";
      }
    });
    return;
  }

  function submitCommentRating(comment_id, rating) {
    $.ajax({
      type: "POST",
      url: "${path_url}/comments/submit-rating?proj_id=${proj_id}",
      data: {
        comment_id: comment_id,
        rating : rating
      },
      success: function(result) {
        var obj = jQuery.parseJSON(result);
        if (obj.result == -1) {
          $("#comment-rating-failure-1").dialog("open");
        } else if (obj.result == -2){
          $("#comment-rating-failure-2").dialog("open");
        } else {
          $("#comment-rating-success").dialog("open");
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
        location.href = "/";
      }
    });
    return;
  }

  function showHideContent(shID) {
    if (document.getElementById(shID)) {
      if (document.getElementById(shID+'-show').style.display != 'none') {
        document.getElementById(shID+'-show').style.display = 'none';
        document.getElementById(shID).style.display = 'block';
      } else {
        document.getElementById(shID+'-show').style.display = 'inline';
        document.getElementById(shID).style.display = 'none';
      }
    }
  }
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div id="checklength-false" title="Error">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry, we are unable to process your request.
    </p>
  </div>
  <div id="project-description-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully editted your project description.
    </p>
  </div>
  <div id="add-comment-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully added a comment.
    </p>
  </div>
  <div id="comment-flag-failure" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have to be logged in to flag a comment.
    </p>
  </div>
  <div id="comment-flag-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully flagged a comment.
    </p>
  </div>
  <div id="comment-rating-failure-1" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have to be logged in to submit a rating for a comment.
    </p>
  </div>
  <div id="comment-rating-failure-2" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have already submitted a rating for a comment.
    </p>
  </div>
  <div id="comment-rating-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully submitted a rating for a comment.
    </p>
  </div>

  <div class="article">
    <h2>${proj_name}</h2>
    <h3>${proj_type} Application</h3>
    <br/>
    <div class="clr"></div>  
    <applet code="org.jdesktop.applet.util.JNLPAppletLauncher"
      width=950 
      height=600
      codebase="http://www.ccd.rpi.edu/eglash/csdt/pcsdt/SB"
      archive="applet-launcher.jar">

      <param name="codebase_lookup" value="true">
      <param name="subapplet.classname" VALUE="SB.SBGui">
      <param name="subapplet.displayname" VALUE="SB Applet">
      <param name="noddraw.check" value="true">
      <param name="progressbar" value="true">

      <param name="jnlp_href" value="${jnlp_path}">
    </applet>
    <p>
      If the applet version above doesn't work, please launch the Web Start version <a href="${jnlp_path}">here</a>.
    </p>
    <div class="rating">
      <ul>
        <li>
          <strong>Your Rating:</strong> 
          <span id="stars-choice-cap" class="rating-cap"></span>
          <form id="stars-choice">
            <select name="selrate" style="width: 160px">
              <option value="1">+1</option>
            </select>
          </form>
        </li>
        <li>
          <strong>Ratings:</strong>
          <span id="stars-average-cap"></span>
          <div id="stars-average-off" class="stars-off" style="width:0"><div id="stars-average-on" class="stars-on" style="width:0"></div></div>
        </li>
      </ul>
    </div>
    <br/><br/><br/>
    <div class="project-info">
      <p>
        <span>Created by:</span> ${username}<br/>
        <span>Published:</span> ${time}<br/>
        <span>Views:</span> ${num_views}<br/>
        <span>Downloads:</span> ${downloads}<br/>
        <%
          if "username" in session and session["username"] == owner:
            context.write("<a href=\"#\" id=\"favorite\">Add as Favorite</a>")
          else:
            context.write("<a href=\"/login\" id=\"favorite\">Add as Favorite</a>")
        %>
        <a href="#" id="flag">Flag project</a>
        <a href="#" id="download">Download Project</a>
      </p>
    </div>
    <div class="proj-desc">
      <br/><br/><br/><br/><br/><br/><br/><br/>
      <h3>Description</h3>
      <%
        if "username" in session and session["username"] == owner:
          context.write("<br/>")
          context.write("<form class=\"cmxform validate-form\" id=\"project-description\" method=\"get\" action=\"\">")
          context.write("<fieldset class=\"fieldset-auto-width\">")
          context.write("<div class=\"field\">")
          context.write("<textarea cols=\"100\" rows=\"3\" id=\"description\" name=\"description\"></textarea>")
          context.write("</div>")
          context.write("<div class=\"button\">")
          context.write("<input class=\"submit\" id=\"project-description-save\" type=\"submit\" value=\"Save\"/>")
          context.write("</div>")
          context.write("</fieldset>")
          context.write("</form>")
          context.write("<br/><br/><br/><br/><br/><br/>")
      %>
      <p>${description}</p>
    </div>
    <div class="commentContainer">
      <p>Post Comment</p>
      <form id="add-comment" method="post" action="">
        <div class="field">
          <label for="body">You need to be logged in to post comments</label>
          <textarea name="body" id="body" cols="20" rows="5"></textarea>
        </div>
        <div class="button">
          <input type="submit" id="comment-submit" value="Post Comment" />
        </div>
      </form>
    </div>
    <div class="align-comment" id="all-comment-posts"></div>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
