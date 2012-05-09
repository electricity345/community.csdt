<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Login</title>
</%block>

<%block name="scripts">
  $(document).ready(function(){
    $("#error-password-login").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "/login";
          $(this).dialog("close"); 
        }
      }
    });

    $("#reg-submit").click(function(){
      $("#login-form-2").submit(function() {
        $.ajax({
          type: "POST",
          url: "/login/login-forms",
          data: {
            login_name : $("input#login_username_page").val(),
            password : $("input#login_password_page").val(),
          },
          success: function(result) {
            var obj = jQuery.parseJSON(result);
            if (obj.result == 0) {
              location.href = "/accounts/" + obj.username;
            } else if (obj.result == -1) {
              $("#error-password-login").dialog("open");
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
  <div id="error-password-login" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry. Either the password does not match or your username does not exist.
    </p>
  </div>

  <div class="article">
    <h2>Login</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="login-form-2" method="get" action="">
      <fieldset class="fieldset-auto-width">
        <div class="field">
          <label for="cname">Username:</label>
          <input id="login_username_page" name="login_name" type="text" size="25" />
        </div>
        <div class="field">
          <label for="cpassword">Password:</label>
          <input id="login_password_page" name="password" type="password" size="25" />
        </div>
        <div class="button">
          <input class="submit" id="reg-submit" type="submit" value="Login"/>
        </div>
      </fieldset>
    </form>
    <br/><br/><br/><br/><br/><br/><br/><br/><br/>
    <p><span>Forget your account <a href="/recover/password">password</a>?</span><br/>
      <span>Don't have an account yet? <a href="/register">Sign up now</a>!</span>
    </p>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
