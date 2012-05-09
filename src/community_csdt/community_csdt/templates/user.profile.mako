<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | ${owner} | Profile</title>
</%block>

<%block name="info">
<div class="content content_resize_main mainbar">
  <div class="icsdt">
    <h2>${owner}'s Profile</h2>
    <%
      if "username" in session and session["username"] == owner:
        context.write("<h3>(<a href=\"/accounts/" + owner + "/admin/profile/edit\">Edit Account Profile</a> | <a href=\"/accounts/" + owner + "/admin/password/edit\">Change Account Password</a>)</h3>")
        
        if "permissions" in session and session["permissions"] == "p":
          context.write("<h3><a href=\"/register/classes/new\">Create a Class</a></h3>")
        
        if "teacher_classes" in session:
          context.write("<h3><a href=\"/accounts/" + owner + "/admin/classes/teacher-all\">Manage Classes</a></h3>")
          context.write("<h3><a href=\"/accounts/" + owner + "/admin/comments/flag-all\">Flagged Comments</a></h3>")

        if "student_classes" in session:
          context.write("<h3><a href=\"/accounts/" + owner + "/admin/classes/student-all\">View Own Classes</a></h3>")
        
        context.write("<h3><a href=\"/register/classes/all\">Join a Class</a></h3>")
    %>
    <h3>About Me</h3>
    <p>${about}</p>
  </div>
</div>

<div class="second-divider">
<div class="second-divider-content body-sticky-footer mainbar">
  <div class="article">
    <div class="clr"></div>
    <h2><a href="/accounts/${owner}/projects">Projects by ${owner}</a></h2>
    <table id="proj_table" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="proj_table_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#proj_table").jqGrid({
          url: '/accounts/${owner}/projects-tables',
          datatype: "json",
          mtype: 'GET',
          <%
            if "username" in session and session["username"] == owner:
              if "student_classes" in session or "teacher_classes" in session:
                context.write("colNames:[\'PID\', \'Thumbnail\', \'Created By\', \'Project Name\', \'Type\', \'Description\', \'Views\', \'Likes\', \'Downloads\', \'Edit\', \'Delete\', \'Copy to Class\', \'Stored Project Name\', \'Published\'],")
              else:
                context.write("colNames:[\'PID\', \'Thumbnail\', \'Created By\', \'Project Name\', \'Type\', \'Description\', \'Views\', \'Likes\', \'Downloads\', \'Edit\', \'Delete\',\'Stored Project Name\', \'Published\'],")
            else:
              context.write("colNames:[\'PID\', \'Thumbnail\', \'Created By\', \'Project Name\', \'Type\', \'Description\', \'Views\', \'Likes\', \'Downloads\', \'Stored Project Name\', \'Published\'],")
          %>
          colModel:[
            {name:'id', index:'id', width:25, sorttype:"int", hidden:true},
            {name:'img', width:80, sortable:false, formatter: imgFormatter},
            {name:'username', index:'username', width:100, sorttype:"string"},
            {name:'proj_name', index:'proj_name', width:150, sorttype:"string"},
            {name:'proj_type', index:'proj_type', width:55, sorttype:"string"},
            <%
              if "username" in session and session["username"] == owner:
                context.write("{name:\'description\', index:\'description\', width:250, sorttype:\"string\"},")
              else:
                context.write("{name:\'description\', index:\'description\', width:300, sorttype:\"string\"},")
            %>
            {name:'num_views', index:'num_views', width:55, sorttype:"int"},
            {name:'ratings', index:'rating', width:55, sorttype:"int"},
            {name:'downloads', index:'table_A.downloads', width:70, sorttype:"int", hidden:true},
            <%
              if "username" in session and session["username"] == owner:
                context.write("{name:\'edit\', width:50, sortable:false, formatter:editFormatter},")
                context.write("{name:\'delete\', width:60, sortable:false, formatter:deleteFormatter},")
                if "student_classes" in session or "teacher_classes" in session:
                  context.write("{name:\'copy\', width:75, sortable:false, formatter:copyFormatter},")
            %>
            {name:'stored_proj_name', hidden:true},
            {name:'time', hidden:true}
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            <%
              if "username" in session and session["username"] == owner:
                context.write("if (iCol == 9) {")
                context.write("location.href=\"/\";")
                context.write("}")
                context.write("else if (iCol == 10) {")
                context.write("location.href=\"/\";")
                context.write("}")

                if "student_classes" in session or "teacher_classes" in session:
                  context.write("else if (iCol == 11) {")
                  context.write("var proj_id = jQuery('#proj_table').jqGrid('getCell', rowid, 0);")
                  context.write("location.href=\"/accounts/" + owner + "/admin/projects/copy-to-class-list?proj_id=\" + proj_id;")
                  context.write("}")

                context.write("else {")
            %>
            
            var projects = new Array();
            projects["proj_id"] = jQuery('#proj_table').jqGrid('getCell', rowid, 0);
            projects["username"] = jQuery('#proj_table').jqGrid('getCell', rowid, 2);
            projects["proj_name"] = jQuery('#proj_table').jqGrid('getCell', rowid, 3);
            projects["proj_type"] = jQuery('#proj_table').jqGrid('getCell', rowid, 4);
            projects["description"] = jQuery('#proj_table').jqGrid('getCell', rowid, 5);
            projects["num_views"] = jQuery('#proj_table').jqGrid('getCell', rowid, 6);
            projects["ratings"] = jQuery('#proj_table').jqGrid('getCell', rowid, 7);
            projects["downloads"] = jQuery('#proj_table').jqGrid('getCell', rowid, 8);

            <%
              if "username" in session and session["username"] == owner:
                if "student_classes" in session or "teacher_classes" in session:
                  context.write("projects[\"stored_proj_name\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 12);")
                  context.write("projects[\"time\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 13);")
                else:
                  context.write("projects[\"stored_proj_name\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 11);")
                  context.write("projects[\"time\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 12);")
              else:
                context.write("projects[\"stored_proj_name\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 9);")
                context.write("projects[\"time\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 10);")
            %>

            createFormAndSubmit(projects);

            <%
              if "username" in session and session["username"] == owner:
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
            id: 'table_A.proj_id'
          },
          rowNum: 20,
          rowList: [20,40,60],
          pager: jQuery('#proj_table_pager'),
          sortname: 'table_A.proj_id',
          viewrecords: true,
          sortorder: "asc",
          caption: "Projects by ${owner}"
        });
        jQuery("#proj_table").jqGrid('navGrid','#proj_table_pager',{edit:false,add:false,del:false});
      }

      function imgFormatter (cellvalue, options, rowObject) {
        var format_value;
        var stored_proj_name = rowObject['stored_proj_name'];
        var proj_type = rowObject['proj_type'];

        var img_file = "<img src= \"/uploads/projects/" + proj_type + "/thumbs/" + stored_proj_name + ".jpg\" />";
        return img_file;
      }

      function editFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Edit</button>";
      }

      function deleteFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Delete</button>";
      }

      function copyFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Copy</button>";
      }

      function createNewFormElement(inputForm, inputName, inputValue){
        var input = document.createElement("input");
        input.setAttribute("name", inputName);
        input.setAttribute("type", "hidden");
        input.setAttribute("value", inputValue);
        inputForm.appendChild(input);
        
        return input;
      }

      function createFormAndSubmit(projects) {
        var submit_form = document.createElement("FORM");
        document.body.appendChild(submit_form);
        submit_form.method = "POST";

        for (key in projects) {
          createNewFormElement(submit_form, key, projects[key]);
        }

        submit_form.action = "/projects?proj_id=" + projects["proj_id"];
        submit_form.submit();
      }

      $(document).ready(function() {
        window.jqinvoke && jqinvoke.call && jqinvoke();
      });
    </script>

    <h2><a href="/accounts/${owner}/projects/favorite">${owner}'s Favorite Projects</a></h2>
    <h2><a href="/accounts/${owner}/friends">${owner}'s Friends</a></h2>
    <h2><a href="/accounts/${owner}/comments">${owner}'s Comments</a></h2>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</div>
</%block>
