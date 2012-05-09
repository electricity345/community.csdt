<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Creating Public User Account</title>
</%block>

<%block name="scripts">
  $(document).ready(function(){
    $("#checkfield-false").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-captcha").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          //Recaptcha.reload();
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-password-registration").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-username").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-email").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    /*Passwords don't need any filters*/
    function checkFields() {
      var username = $("input#username").val();
      var password = $("input#password").val(); 
      var re_password = $("input#re_password").val();
   
      var check_space = /\s/;
      if (check_space.test(username) == true) {
        return false;
      }

      if (username.length < 6 || username.length > 30 || password.length < 6 || password.length > 30 || re_password.length < 6 || re_password.length > 30) {
        return false;
      }

      var username_filter = /^[a-zA-Z][a-zA-Z0-9]*\.?[a-zA-Z0-9]*$/;
      if (username_filter.test(username) == false) {
        return false;
      }

      return true;
    }

    $("#registerForm").validate({
      rules: {
        username: {
          required: true,
          minlength: 6,
          maxlength: 30,
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
        username: {
          required: "Please enter a username",
          minlength: "Your username must be at least 6 characters long",
          maxlength: "Your username must be no more than 30 characters long"
        },
        password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 6 characters long",
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
    
    /*Checks username availability*/
    $("#login-check").click(function(){
      var username = $("input#username").val();
      var check_space = /\s/;
      if (check_space.test(username)) {
        content = "<p>Required field cannot be left blank. Only letters (a-z), numbers (0-9), and periods (.) are allowed.</p>";
        $("#check-username").empty(); 
        $(content).appendTo("#check-username");
        return false;
      }

      if (username.length < 6 || username.length > 30) {
        content = "<p>Sorry, your username must be between 6 and 30 characters long.</p>";
        $("#check-username").empty(); 
        $(content).appendTo("#check-username");
        return false;
      }

      var filter = /^[a-zA-Z][a-zA-Z0-9]*\.?[a-zA-Z0-9]*$/;
      if (filter.test(username) == false) {
        content = "<p>Only letters (a-z), numbers (0-9), and periods (.) are allowed. The first character of your username must be an ascii letter (a-z)</p>";
        $("#check-username").empty(); 
        $(content).appendTo("#check-username");
        return false;
      }

      $.ajax({
        type: "POST",
        url: "/register/accounts/check-username",
        data: {
          username : $("input#username").val()
        },
        success: function(result) {
          var obj = jQuery.parseJSON(result);
          if (obj.result == 0) {
            content = "<p>" + username + " is available" + "</p>";
          } else if (obj.result == -1) {
            content = "<p>" + username + " is not available." + "</p>";
          }
          $("#check-username").empty(); 
          $(content).appendTo("#check-username");
        },
        error: function(jqXHR, textStatus, errorThrown) {
          alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
          location.href = "/";
        }
      });
      return false;
    });

    $("#accept-terms").click(function(){
      $("#registerForm").submit(function() {
        if (checkFields() == false) {
          $("#checkfield-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "/register/accounts/public/new-forms",
          data: {
            first_name : "${first_name}",
            last_name : "${last_name}",
            username : $("input#username").val(),
            password : $("input#password").val(),
            re_password : $("input#re_password").val(),
            email : "${email}",
            recaptcha_challenge_field: $("input#recaptcha_challenge_field").val(),
            recaptcha_response_field: $("input#recaptcha_response_field").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              location.href = "/accounts/" + obj.username;
            } else if (obj.result == -1) {
              $("#error-captcha").dialog("open");
            } else if (obj.result == -2) {
              $("#error-password-registration").dialog("open");
            } else if (obj.result == -3) {
              $("#error-username").dialog("open");
            } else if (obj.result == -4) {
              $("#error-email").dialog("open");
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
  <div id="checkfield-false" title="Error">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry, we are unable to process your request.
    </p>
  </div>
  <div id="error-captcha" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Let's try that captcha again.
    </p>
  </div>
  <div id="error-password-registration" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Password does not match.
    </p>
  </div>
  <div id="error-username" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Username already exists.
    </p>
  </div>
  <div id="error-email" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Email already exists.
    </p>
  </div>

  <div class="article">
    <h2>Create a Public User Account</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="registerForm" method="get" action="">
      <fieldset>
        <div class="field">
          <label for="cname">Username:</label>
          <input id="username" name="username" type="text" size="25" value="" />
        </div>
        <div class="field">
          <input class="submit" id="login-check" type="submit" value="Check for Availability"/>
        </div>
        <div class="field" id="check-username"></div>
        <div class="field">
          <label for="cpassword">Password:</label>
          <input id="password" name="password" type="password" size="25" value="" />
        </div>
        <div class="password-meter">
          <div class="password-meter-message"></div>
          <div class="password-meter-bg">
            <div class="password-meter-bar"></div>
          </div>
        </div>
        <div class="field">
          <label for="cpassword">Re-enter Password:</label>
          <input id="re_password" name="re_password" type="password" size="25" value="" />
        </div>
        <div class="field">
          <script type="text/javascript">
            var RecaptchaOptions = {
              theme: 'blackglass'
            };
          </script>
          <script type="text/javascript"
            src="http://www.google.com/recaptcha/api/challenge?k=6Ldi2MYSAAAAAPnmLnh28b0rS0Ol2dweFDsxB0NM">
          </script>
          <noscript>
            <iframe src="http://www.google.com/recaptcha/api/noscript?k=6Ldi2MYSAAAAAPnmLnh28b0rS0Ol2dweFDsxB0NM"
              height="300" width="500" frameborder="0"></iframe><br>
            <textarea id="recaptcha_challenge_field" name="recaptcha_challenge_field" rows="3" cols="40">
            </textarea>
            <input type="hidden" id="recaptcha_response_field" name="recaptcha_response_field"
              value="manual_challenge">
          </noscript>
        </div>
        <div class="field">
          <p>By Clicking "I Accept", you are agreeing to adhere to our <a href="/pages/terms">Terms of Service</a></p>
        </div>
        <div class="field">
          <input class="submit" id="accept-terms" type="submit" value="I Accept"/>
        </div>
      </fieldset>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
