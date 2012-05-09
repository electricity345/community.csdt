<%inherit file="base.html"/>

<%block name="title">
  <%
    if "username" in session and session["username"] == owner:
      context.write("<title>CSDT Community | Managing Class: " + classname + "</title>")
    else:
      context.write("<title>CSDT Community | Viewing Class: " + classname +"</title>")
  %>
</%block>

<%block name="scripts">
  $(document).ready(function(){
    $("#reset-password-flag").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${path_url}?class_id=${class_id}";
          $(this).dialog("close"); 
        }
      }
    });
  });
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div id="reset-password-flag" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully reset the user's password.
    </p>
  </div>

  <div class="article">
    <%
      if "username" in session and session["username"] == owner:
        context.write("<h2>Managing Class: " + classname + "</h2>")
      else:
        context.write("<h2>Viewing Students in Class</h2>")
    %>
    <div class="clr"></div>
    <table id="class_table" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="class_table_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript">
      function jqinvoke() {
        function resetPasswordFlag(student_user_id) {
          $.ajax({
            type: "POST",
            url: "/classes/set-password-flag?class_id=${class_id}&user_id=" + student_user_id,
            success: function(result) {
              var obj = jQuery.parseJSON(result);
              if (obj.result == 0) {
                $("#reset-password-flag").dialog("open");
              }
            },
            error: function(jqXHR, textStatus, errorThrown) {
              alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
              location.href = "/";
            }
          });

          return false;
        }

        jQuery("#class_table").jqGrid({
          url: '/classes/students-all-tables?class_id=${class_id}',
          datatype: "json",
          mtype: 'GET',
          <%
            if "username" in session and session["username"] == owner:
              context.write("colNames:[\'User Id\', \'Username\', \'First Name\', \'Last Name\', \'Name\', \'View Projects\', \'View Profile\', \'Reset Password\', \'Delete User\'],")
            else:
              context.write("colNames:[\'User Id\', \'Username\', \'First Name\', \'Last Name\', \'Name\', \'View Projects\', \'View Profile\'],")
          %>
          colModel:[
            {name:'user_id', hidden:true},
            {name:'username', index:'username', width:200, sorttype:"string"},
            {name:'first_name', index:'first_name', width:200, sorttype:"string", hidden:true},
            {name:'last_name', index:'last_name', width:200, sorttype:"string", hidden:true},
            {name:'full_name', index:'last_name', width:150, sorttype:"string"},
            {name:'projects', width:80, sortable:false, formatter:projectFormatter},
            {name:'view', width:80, sortable:false, formatter:profileFormatter},
            <%
              if "username" in session and session["username"] == owner:
                context.write("{name:\'reset_password\', width:100, sortable:false, formatter:resetPasswordFormatter},")
                context.write("{name:\'delete\', width:80, sortable:false, formatter:deleteFormatter},")
            %>
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            if (iCol == 5) {
              var username = jQuery('#class_table').jqGrid('getCell', rowid, 1);
              location.href="/accounts/" + username + "/projects";
            } else if (iCol == 6) {
              var username = jQuery('#class_table').jqGrid('getCell', rowid, 1);
              location.href="/accounts/" + username;
            } 
            <%
              if "username" in session and session["username"] == owner:
                context.write("else if (iCol == 7) {")
                context.write("var user_id = jQuery(\'#class_table\').jqGrid(\'getCell\', rowid, 0);")
                context.write("resetPasswordFlag(user_id);")
                context.write("}")
                context.write("else if (iCol == 8) {")
                context.write("var user_id = jQuery(\'#class_table\').jqGrid(\'getCell\', rowid, 0);")
                context.write("location.href=\"/\";")
                context.write("}")
            %>
            return false;
          }, 
          jsonReader : {
            root: 'results',
            page: 'page',
            total: 'total',
            records: 'records',
            repeatitems: false,
            id: 'u.first_name'
          },
          rowNum: 20,
          rowList: [20,40,60],
          pager: jQuery('#class_table_pager'),
          sortname: 'u.first_name',
          viewrecords: true,
          sortorder: "asc",
          <%
            if "username" in session and session["username"] == owner:
              context.write("caption: \"Managing Students in Class\"")
            else:
              context.write("caption: \"Viewing Students in Class\"")
          %>
        });
        jQuery("#class_table").jqGrid('navGrid','#class_table_pager',{edit:false,add:false,del:false});
      }

      function projectFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Projects</button>";
      }

      function profileFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Profiles</button>";
      }

      function resetPasswordFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Reset</button>";
      }

      function deleteFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Delete</button>";
      }

      $(document).ready(function() {
        window.jqinvoke && jqinvoke.call && jqinvoke();
      });
    </script>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
