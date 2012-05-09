<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Classroom | Edit Class Description</title>
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

    $("#edit-description-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/classes?class_id=${class_id}";
          $(this).dialog("close"); 
        }
      }
    });

    function checkLength() {
      var description = $("textarea#description").val();
      
      if (description.length > 200) {
        return false;
      }

      return true;
    }

    $("#edit-description").validate({
      rules: {
        description: {
          maxlength: 200
        }
      },
      messages: {
        description: {
          maxlength: "Your classroom description must be no more than 200 characters long"
        }
      }
    });

    $("#edit-description-save").click(function(){
      $("#edit-description").submit(function() {
        if (checkLength() == false) {
          $("#checklength-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "${path_url}-forms?class_id=${class_id}",
          data: {
            description : $("textarea#description").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              $("#edit-description-success").dialog("open");
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
  <div id="edit-description-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully editted your classroom description.
    </p>
  </div>

  <div class="article">
    <h2>Classroom Settings</h2>
    <h3><a href="${full_url}">Edit Class Description</a> | <a href="/classes/password/edit?class_id=${class_id}">Change Class Password</a> | <a href="/classes/comments/edit-flag-level?class_id=${class_id}">Edit Class Comment Flag Level</a></h3>
    <br/>
    <h2>Edit Class Description</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="edit-description" method="get" action="">
      <fieldset class="fieldset-auto-width">
        <div class="field">
          <label for="cabout">Class Description</label>
          <textarea cols="40" rows="5" id="description" name="description"></textarea>
        </div>
        <div class="button">
          <input class="submit" id="edit-description-save" type="submit" value="Save"/>
        </div>
      </fieldset>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
