<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Password Recovery</title>
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

    $("#recover-pass-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-captcha").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${path_url}";
          //Recaptcha.reload();
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-recover-pass").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${path_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-recover-pass-student").dialog({
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
      var input_string = $("input#input_string").val();
   
      if (input_string.length == 0 || input_string.length > 100) {
        return false;
      }

      return true;
    }

    $("#recover-account").click(function(){
      $("#password-recovery").submit(function() {
        if (checkLength() == false) {
          $("#checklength-false").dialog("open");
          return false;
        }

        $.ajax({
          type: "POST",
          url: "${path_url}-forms",
          data: {
            input_string : $("input#input_string").val(),
            recaptcha_challenge_field: $("input#recaptcha_challenge_field").val(),
            recaptcha_response_field: $("input#recaptcha_response_field").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 1) {
              location.href = obj.url;
            } else if (obj.result == 0) {
              $("#recover-pass-success").dialog("open");
            } else if (obj.result == -1) {
              $("#error-captcha").dialog("open");
            } else if (obj.result == -2) {
              $("#error-recover-pass-student").dialog("open");
            } else if (obj.result == -3) {
              $("#error-recover-pass").dialog("open");
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
  <div id="recover-pass-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      A recovery token has been sent to your email address.
    </p>
  </div>
  <div id="error-captcha" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Let's try that captcha again.
    </p>
  </div>
  <div id="error-recover-pass" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry. Either the username or the email address does not exist. Please try again.
    </p>
  </div>
  <div id="error-recover-pass-student" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry. Please ask one of your teachers to reset your password before you can change your password.
    </p>
  </div>

  <div class="article">
    <h2>Password Recovery</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="password-recovery" method="get" action="">
      <fieldset class="fieldset-auto-width">
        <div class="field">
          <label for="cname">Enter your Username or Email:</label>
          <input id="input_string" name="input_string" type="text" size="25" />
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
        <div class="button">
          <input class="submit" id="recover-account" type="submit" value="Recover Password"/>
        </div>
      </fieldset>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
