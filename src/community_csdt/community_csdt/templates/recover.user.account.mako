<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Change Password</title>
</%block>

<%block name="scripts">
  $(document).ready(function(){
    $("#checklength-false").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${path_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#password-reset-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/accounts/${username}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-password-reset").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${path_url}";
          $(this).dialog("close"); 
        }
      }
    });

    function checkLength() {
      var password = $("input#password").val(); 
      var re_password = $("input#re_password").val();
   
      if (password.length < 6 || password.length > 30 || re_password.length < 6 || re_password.length > 30) {
        return false;
      }

      return true;
    }

    $("#password-reset").validate({
      rules: {
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
        password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 6 characters long"
        },
        re_password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 6 characters long",
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
          url: "${path_url}-forms",
          data: {
            password : $("input#password").val(),
            re_password : $("input#re_password").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              $("#password-reset-success").dialog("open");
            } else if (obj.result == -1) {
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
  <div id="error-password-reset" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry. Either the password is not legal or the re-entered password does not match the inital password.
    </p>
  </div>

  <div class="article">
    <h2>Change Password</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="password-reset" method="get" action="">
      <fieldset class="fieldset-auto-width">
        <div class="field">
          <label for="password">Password</label>
          <input id="password" name="password" type="password" size="25" />
        </div>
        <div class="field">
          <label for="re_password">Re-enter Password:</label>
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
