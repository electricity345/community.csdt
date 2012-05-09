<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Classroom | Change Class Password</title>
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

    $("#password-reset-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/classes?class_id=${class_id}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-password-original").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-password-reset").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    function checkLength() {
      var original_password = $("input#original_password").val();
      var password = $("input#password").val(); 
      var re_password = $("input#re_password").val();
   
      if (original_password.length == 0 || original_password.length > 30 || password.length < 6 || password.length > 30 || re_password.length < 6 || re_password.length > 30) {
        return false;
      }

      return true;
    }

    $("#password-reset").validate({
      rules: {
        original_password: {
          required: true,
          maxlength: 30
        },
        password: {
          required: true,
          minlength: 6,
          maxlength: 30
        },
        re_password: {
          required: true,
          equalTo: "#password",
          minlength: 6,
          maxlength: 30
        }
      },
      messages: {
        original_password: {
          required: "Please provide your original password",
          maxlength: "Your password must be no more than 30 characters long"
        },
        password: {
          required: "Please provide a password",
          maxlength: "Your password must be no more than 30 characters long"
        },
        re_password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 6 characters long",
          maxlength: "Your password must be no more than 30 characters long",
          equalTo: "Please enter the same password as above"
        }
      }
    });

    $("#new-password").click(function(){
      $("#password-reset").submit(function() {
        if (checkLength() == false) {
          $("#checklength-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "${path_url}-forms?class_id=${class_id}",
          data: {
            original_password: $("input#original_password").val(),
            password : $("input#password").val(),
            re_password : $("input#re_password").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              $("#password-reset-success").dialog("open");
            } else if (obj.result == -1) {
              $("#error-password-original").dialog("open");
            } else if (obj.result == -2) {
              $("#error-password-reset").dialog("open");
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
  <div id="password-reset-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully reset your password.
    </p>
  </div>
  <div id="error-password-original" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry. Your original password does not match the one stored in the database.
    </p>
  </div>
  <div id="error-password-reset" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry. Either the password is not legal or the re-entered password does not match the inital password.
    </p>
  </div>

  <div class="article">
    <h2>Classroom Settings</h2>
    <h3><a href="/classes/description/edit?class_id=${class_id}">Edit Class Description</a> | <a href="${full_url}">Change Class Password</a> | <a href="/classes/comments/edit-flag-level?class_id=${class_id}">Edit Class Comment Flag Level</a></h3>
    <br/>
    <h2>Change Class Password</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="password-reset" method="get" action="">
      <fieldset class="fieldset-auto-width">
        <div class="field">
          <label for="original_password">Original Password</label>
          <input id="original_password" name="original_password" type="password" size="25" />
        </div>
        <div class="field">
          <label for="password">Password</label>
          <input id="password" name="password" type="password" size="25" />
        </div>
        <div class="field">
          <label for="re_password">Re-enter Password</label>
          <input id="re_password" name="re_password" type="password" size="25" />
        </div>
        <div class="button">
          <input class="submit" id="new-password" type="submit" value="Save"/>
        </div>
      </fieldset>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
