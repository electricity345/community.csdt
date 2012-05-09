<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Registering as Public User</title>
</%block>

<%block name="scripts">
  $(document).ready(function(){
    $("#checkfield-false").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/register/accounts/public";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-captcha").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/register/accounts/public";
          //Recaptcha.reload();
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-email").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/register/accounts/public";
          $(this).dialog("close"); 
        }
      }
    });

    function checkFields() {
      var first_name = $("input#first_name").val();
      var last_name = $("input#last_name").val();
      var email = $("input#email").val();
   
      var check_space = /\s/;
      if (check_space.test(first_name) == true || check_space.test(last_name) == true || check_space.test(email) == true) {
        return false;
      }

      if (first_name.length < 1 || first_name.length > 30 || last_name.length < 1 || last_name.length > 30 || email.length < 1 || email.length > 45) {
        return false;
      }

      var name_filter = /^[a-zA-Z]+$/
      if (name_filter.test(first_name) == false || name_filter.test(last_name) == false) {
        return false;
      }

      var email_filter = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i;      
      if (email_filter.test(email) == false) {
        return false;
      }

      return true;
    }

    $("#registerForm").validate({
      rules: {
        first_name: {
          required: true,
          maxlength: 30
        },
        last_name: {
          required: true,
          maxlength: 30
        },
        email: {
          required: true,
          email: true,
          maxlength: 45
        }
      },
      messages: {
        first_name: {
          required: "Please enter your first name",
          maxlength: "Your first name must be no more than 30 characters long"
        },
        last_name: {
          required: "Please enter your last name",
          maxlength: "Your last name must be no more than 30 characters long"
        },
        email: {
          required: "Please enter a valid email address",
          maxlength: "Your email must be no more than 45 characters long"
        }
      }
    });
    
    $("#accept-terms").click(function(){
      $("#registerForm").submit(function() {
        if (checkFields() == false) {
          $("#checkfield-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "/register/accounts/public/forms",
          data: {
            first_name : $("input#first_name").val(),
            last_name : $("input#last_name").val(),
            email : $("input#email").val(),
            recaptcha_challenge_field: $("input#recaptcha_challenge_field").val(),
            recaptcha_response_field: $("input#recaptcha_response_field").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              location.href = "/";
            } else if (obj.result == -1) {
              $("#error-captcha").dialog("open");
            } else if (obj.result == -2) {
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
  <div id="error-email" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Email already exists.
    </p>
  </div>

  <div class="article">
    <h2>Register For a Public User Account</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="registerForm" method="get" action="">
      <fieldset>
        <div class="field">
          <label for="cname">First Name:</label>
          <input id="first_name" name="first_name" type="text" size="25" value="" />
        </div>
        <div class="field">
          <label for="cname">Last Name:</label>
          <input id="last_name" name="last_name" type="text" size="25" value="" />
        </div>
        <div class="field">
          <label for="cemail">E-Mail:</label>
          <input id="email" name="email" type="text" size="25" class="required email" />
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
