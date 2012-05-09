<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | ${classname}'s Class Sign-up</title>
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

    $("#error-password-class-signup").dialog({
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
      var password = $("input#password").val(); 
      if (password.length == 0 || password.length > 100) {
        return false;
      }

      return true;
    }

    $("#loginForm").submit(function() {
      if (checkFields() == false) {
        $("#checkfield-false").dialog("open");
        return false;
      }

      $.ajax({
        type: "POST",
        url: "${path_url}-forms?class_id=${class_id}",
        data: {
          password : $("input#password").val()
        },
        success: function(result) {
          var obj = jQuery.parseJSON(result);
          if (obj.result == 0) {
            <%
              if "username" in session:
                context.write("location.href=\"/accounts/" + session["username"] + "/admin/classes/student-all\";")
              else:
                context.write("location.href=\"/register/accounts/student/new?class_id=" + class_id +"\";")
            %>
          } else if (obj.result == -1) {
            $("#error-password-class-signup").dialog("open");
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
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div id="checkfield-false" title="Error">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry, we are unable to process your request.
    </p>
  </div>
  <div id="error-password-class-signup" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      Sorry. The password does not match the class' password.
    </p>
  </div>

  <div class="article">
    <h2>${classname}'s Class Sign-up</h2>
    <div class="clr"></div>
    <form class="cmxform validate-form" id="loginForm" method="get" action="">
      <fieldset class="fieldset-auto-width">
        <div class="field">
          <label for="cpassword">Password:</label>
          <input id="password" name="password" type="password" size="25" value="" />
        </div>
        <div class="button">
          <input class="submit" id="reg-submit" type="submit" value="Submit"/>
        </div>
      </fieldset>
    </form>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
