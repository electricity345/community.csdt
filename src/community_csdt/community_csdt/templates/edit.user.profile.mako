<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | ${owner} | Edit Account Profile</title>
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

    $("#edit-profile-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/accounts/${owner}";
          $(this).dialog("close"); 
        }
      }
    });

    function checkLength() {
      var about = $("textarea#about").val();
      
      if (about.length > 200) {
        return false;
      }

      return true;
    }

    $("#edit-profile").validate({
      rules: {
        about: {
          maxlength: 200
        }
      },
      messages: {
        about: {
          maxlength: "Your username must be no more than 200 characters long"
        }
      }
    });

    $("#edit-profile-save").click(function(){
      $("#edit-profile").submit(function() {
        if (checkLength() == false) {
          $("#checklength-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "${path_url}-forms",
          data: {
            about : $("textarea#about").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              $("#edit-profile-success").dialog("open");
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
  <div id="edit-profile-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully editted your profile.
    </p>
  </div>

  <div class="article">
    <h2>Account Settings</h2>
    <h3><a href="${full_url}">Edit Account Profile</a> | <a href="/accounts/${owner}/admin/password/edit">Change Account Password</a> | <a href="/accounts/${owner}/admin/email/edit">Change Account Email</a></h3>
    <br/>
    <h2>Edit Account Profile</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="edit-profile" method="get" action="">
      <fieldset class="fieldset-auto-width">
        <div class="field">
          <label for="cabout">About Me</label>
          <textarea cols="40" rows="5" id="about" name="about"></textarea>
        </div>
        <div class="button">
          <input class="submit" id="edit-profile-save" type="submit" value="Save"/>
        </div>
      </fieldset>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
