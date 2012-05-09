<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Classroom | ${classname}</title>
</%block>

<%block name="info">
<div class="content content_resize_main mainbar">
  <div class="icsdt">
    <h2>${classname}</h2>
    <%
      if "username" in session and session["username"] == owner:
        context.write("<h3>(<a href=\"/classes/description/edit?class_id=" + class_id +  "\">Edit Class Description</a> | <a href=\"/classes/password/edit?class_id=" + class_id +  "\">Change Class Password</a> | <a href=\"/classes/comments/edit-flag-level?class_id=" + class_id +  "\">Edit Class Flag Level</a>)</h3>")
        context.write("<h3>(<a href=\"/classes/students-all?class_id=" + class_id + "\">Manage All Students</a>)</h3><br/>")
      else:
        context.write("<h3>(<a href=\"/classes/students-all?class_id=" + class_id + "\">All Students</a>)</h3><br/>")
    %>
    <h3>Classroom Description</h3>
    <p>${about}</p>
    <h3>Owner: <a href="/accounts/${owner}">${owner}</a></h3>
    <h3>Created: <span>${created}</span></h>
  </div>
</div>

<div class="second-divider">
<div class="second-divider-content body-sticky-footer mainbar">
  <div class="article">
    <div class="clr"></div>
    <h2><a href="/accounts/${owner}/projects">Projects in ${classname}</a></h2>
    <table id="proj_table" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="proj_table_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#proj_table").jqGrid({
          url: '/classes/projects-tables?class_id=${class_id}',
          datatype: "json",
          mtype: 'GET',
          <%
            if "username" in session and session["username"] == owner:
              context.write("colNames:[\'PID\', \'Thumbnail\', \'Created By\', \'Project Name\', \'Type\', \'Description\', \'Views\', \'Likes\', \'Downloads\', \'Edit\', \'Delete\',\'Stored Project Name\', \'Published\'],")
            else:
              context.write("colNames:[\'PID\', \'Thumbnail\', \'Created By\', \'Project Name\', \'Type\', \'Description\', \'Views\', \'Likes\', \'Downloads\', \'Stored Project Name\', \'Published\'],")
          %>
          colModel:[
            {name:'id', index:'table_A.proj_id', width:25, sorttype:"int", hidden:true},
            {name:'img', width:80, sortable:false, formatter: imgFormatter},
            {name:'username', index:'table_A.username', width:100, sorttype:"string"},
            {name:'proj_name', index:'table_A.proj_name', width:150, sorttype:"string"},
            {name:'proj_type', index:'table_A.proj_type', width:45, sorttype:"string"},
            <%
              if "username" in session and session["username"] == owner:
                context.write("{name:\'description\', index:\'table_A.description\', width:250, sorttype:\"string\"},")
              else:
                context.write("{name:\'description\', index:\'table_A.description\', width:300, sorttype:\"string\"},")
            %>
            {name:'num_views', index:'table_A.num_views', width:45, sorttype:"int"},
            {name:'ratings', index:'rating', width:45, sorttype:"int"},
            {name:'downloads', index:'table_A.downloads', width:70, sorttype:"int", hidden:true},
            <%
              if "username" in session and session["username"] == owner:
                context.write("{name:\'edit\', width:50, formatter:editFormatter},")
                context.write("{name:\'delete\', width:60, formatter:deleteFormatter},")
            %>
            {name:'stored_proj_name', hidden:true},
            {name:'time', hidden:true}
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
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
                context.write("projects[\"stored_proj_name\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 11);")
                context.write("projects[\"time\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 12);")
              else:
                context.write("projects[\"stored_proj_name\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 9);")
                context.write("projects[\"time\"] = jQuery(\'#proj_table\').jqGrid(\'getCell\', rowid, 10);")
            %>

            createFormAndSubmit(projects);
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
          caption: "Projects in ${classname}"
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

    <h2><a href="#">${classname}'s Fans</a></h2>
    <h2><a href="#">${classname}'s Comments</a></h2>
  </div>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</div>
</%block>
