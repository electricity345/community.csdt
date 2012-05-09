<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Classroom | Edit Class Comment Flag Level</title>
</%block>

<%block name="scripts">
  $(document).ready(function(){
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

    $("#flag-level-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#submit-flag-level").click(function(){
      $("#flag-comments-level").submit(function() {
        $.ajax({
          type: "POST",
          url: "/classes/comments/flag-forms?class_id=${class_id}",
          data: {
            level: $("input[type='radio']:checked", "#flag-comments-level").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              $("#flag-level-success").dialog("open");
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

    function getSelectedFlagLevel() {
      $.ajax({
        type: "POST",
        url: "/classes/comments/flag-level?class_id=${class_id}",
        success: function(result) {
          var obj = jQuery.parseJSON(result);
          result = obj.result;
          if (result == 0) {
            content = "<input type=\"radio\" name=\"level\" value=\"0\" checked=\"checked\">None</input> <input type=\"radio\" name=\"level\" value=\"1\">Partial</input> <input type=\"radio\" name=\"level\" value=\"2\"> Full</input>";
            $(content).appendTo("#flag-comment-radio");
          } else if (result == 1) {
            content = "<input type=\"radio\" name=\"level\" value=\"0\">None</input> <input type=\"radio\" name=\"level\" value=\"1\" checked=\"checked\">Partial</input> <input type=\"radio\" name=\"level\" value=\"2\"> Full</input>";
            $(content).appendTo("#flag-comment-radio");
          } else if (result == 2) {
            content = "<input type=\"radio\" name=\"level\" value=\"0\">None</input> <input type=\"radio\" name=\"level\" value=\"1\">Partial</input> <input type=\"radio\" name=\"level\" value=\"2\" checked=\"checked\">Full</input>";
            $(content).appendTo("#flag-comment-radio");
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

    getSelectedFlagLevel();
  });
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div id="checklength-false" title="Error">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry, we are unable to process your request.
    </p>
  </div>
  <div id="flag-level-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully changed the comment flag level of the class.
    </p>
  </div>

  <div class="article">
    <h2>Classroom Settings</h2>
    <h3><a href="/classes/description/edit?class_id=${class_id}">Edit Class Description</a> | <a href="/classes/password/edit?class_id=${class_id}">Change Class Password</a> | <a href="${full_url}">Edit Class Comment Flag Level</a></h3>
    <br/>
    <h2>Edit Class Comment Flag Level</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="flag-comments-level" method="get" action="">
      <div class="field">
        <label for="public">Comment Flag Level</label>
        <div id="flag-comment-radio"></div>
      </div>
      <div class="button">
          <input class="submit" id="submit-flag-level" type="submit" value="Save"/>
      </div>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
