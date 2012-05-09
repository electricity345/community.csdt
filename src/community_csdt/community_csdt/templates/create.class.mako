<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Create a Classroom</title>
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

    $("#error-captcha-create-class").dialog({
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

    $("#error-password-create-class").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#error-classname-create-class").dialog({
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
      var classname = $("input#classname").val();
      classname = classname.replace(/^\s+/g,"");//remove heading whitespace
      classname = classname.replace(/\s+$/g,"");//remove trailing whitespace

      var password = $("input#password").val(); 
      var re_password = $("input#re_password").val();

      if (classname == "") {
        return false;
      }

      if (classname.length < 2 || classname.length > 30 || password.length < 6 || password.length > 30 || re_password.length < 6 || re_password.length > 30) {
        return false;
      }

      return true;
    }

    $("#registerForm").validate({
      rules: {
        classname: {
          required: true,
          minlength: 2,
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
        classname: {
          required: "Please enter a class name",
          minlength: "Your classname must be at least 2 characters long"
        },
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
    
    /*Checks classname availability*/
    $("#login-check").click(function(){
      var classname = $("input#classname").val();
      classname = classname.replace(/^\s+/g,"");//remove heading whitespace
      classname = classname.replace(/\s+$/g,"");//remove trailing whitespace

      if (classname == "") {
        content = "<p>Required field cannot be left blank.</p>";
        $("#check-classname").empty(); 
        $(content).appendTo("#check-classname");
        return false;
      }

      if (classname.length < 2 || classname.length > 30) {
        content = "<p>Sorry, your classname must be between 2 and 30 characters long.</p>";
        $("#check-classname").empty(); 
        $(content).appendTo("#check-classname");
        return false;
      }

      $.ajax({
        type: "POST",
        url: "/register/classes/check-classname",
        data: {
          classname : $("input#classname").val()
        },
        success: function(result) {
          var obj = jQuery.parseJSON(result);
          if (obj.result == 0) {
            content = "<p>" + classname + " is available" + "</p>";
          } else if (obj.result == -1) {
            content = "<p>" + classname + " is not available." + "</p>";
          }
          $("#check-classname").empty(); 
          $(content).appendTo("#check-classname");
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

        var classname = $("input#classname").val();
        classname = classname.replace(/^\s+/g,"");//remove heading whitespace
        classname = classname.replace(/\s+$/g,"");//remove trailing whitespace

        $.ajax({
          type: "POST",
          url: "${full_url}-forms",
          data: {
            classname : classname,
            comment_flag_level: $("input[type='radio']:checked", "#registerForm").val(),
            password : $("input#password").val(),
            re_password : $("input#re_password").val(),
            recaptcha_challenge_field: $("input#recaptcha_challenge_field").val(),
            recaptcha_response_field: $("input#recaptcha_response_field").val()
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              location.href = "/accounts/" + obj.owner + "/admin/classes/teacher-all";
            } else if (obj.result == -1) {
              $("#error-captcha-create-class").dialog("open");
            } else if (obj.result == -2) {
              $("#error-password-create-class").dialog("open");
            } else if (obj.result == -3) {
              $("#error-classname-create-class").dialog("open");
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
  <div id="error-captcha-create-class" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Let's try that captcha again.
    </p>
  </div>
  <div id="error-password-create-class" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Password does not match.
    </p>
  </div>
  <div id="error-classname-create-class" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Classname already exists.
    </p>
  </div>

  <div class="article">
    <h2>Create a Classroom</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="registerForm" method="get" action="">
      <fieldset>
        <div class="field">
          <label for="cname">Class Name:</label>
          <input id="classname" name="classname" type="text" size="25" class="required" minlength="6" />
        </div>
        <div class="field">
          <input class="submit" id="login-check" type="submit" value="Check for Availability"/>
        </div>
        <div class="field" id="check-classname"></div>
        <div class="field">
          <label for="flag_level">Comment Flag Level</label>
          <input type="radio" name="level" value="0" checked="checked">None</input> 
          <input type="radio" name="level" value="1">Partial</input> 
          <input type="radio" name="level" value="2"> Full</input>
        </div>
        <div class="field">
          <label for="cpassword">Password:</label>
          <input id="password" name="password" type="password" size="25" class="required" />
        </div>
        <div class="password-meter">
          <div class="password-meter-message"></div>
          <div class="password-meter-bg">
            <div class="password-meter-bar"></div>
          </div>
        </div>
        <div class="field">
          <label for="cpassword">Re-enter Password:</label>
          <input id="re_password" name="re_password" type="password" size="25" class="required" />
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
          <input class="submit" id="accept-terms" type="submit" value="I Accept"/>
        </div>
      </fieldset>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
