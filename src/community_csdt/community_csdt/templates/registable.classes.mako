<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Join a Class</title>
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div class="article">
    <h2>All Joinable Classes</h2>
    <div class="clr"></div>
    <table id="class_table" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="class_table_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#class_table").jqGrid({
          <%
            if "user_id" in session:
              context.write("url: \'/register/classes/all-registerable-tables?user_id=" + session["user_id"] + "\',")
            else:
              context.write("url: \'/register/classes/all-tables\',")
          %>
          datatype: "json",
          mtype: 'GET',
          <%
            if "user_id" in session:
              context.write("colNames:[\'CID\', \'Classname\', \'# Students\', \'Owner Username\', \'Owner First Name\', \'Owner Last Name\', \'Owner Name\', \'View Class\', \'Register\', \'Has Registered\'],")
            else:
              context.write("colNames:[\'CID\', \'Classname\', \'# Students\', \'Owner Username\', \'Owner First Name\', \'Owner Last Name\', \'Owner Name\', \'View Class\', \'Register\'],")
          %>
          colModel:[
            <%
              if "user_id" in session:
                context.write("{name:\'cid\', index:\'cid\', width:25, sorttype:\"int\", hidden:true},")
                context.write("{name:\'classname\', index:\'classname\', width:150, sorttype:\"string\"},")
                context.write("{name:\'size\', index:\'size\', width:85, sorttype:\"int\"},")
                context.write("{name:\'username\', index:\'username\', width:150, sorttype:\"string\"},")
                context.write("{name:\'first_name\', index:\'first_name\', width:150, sorttype:\"string\", hidden:true},")
                context.write("{name:\'last_name\', index:\'last_name\', width:150, sorttype:\"string\", hidden:true},")
                context.write("{name:\'full_name\', index:\'last_name\', width:150, sorttype:\"string\"},")
                context.write("{name:\'view\', width:60, sortable:false, formatter:viewFormatter},")
                context.write("{name:\'register\', width:60, sortable:false, formatter:registerFormatter},")
                context.write("{name:\'user_id\', hidden:true}")
              else:
                context.write("{name:\'cid\', index:\'cid\', width:25, sorttype:\"int\", hidden:true},")
                context.write("{name:\'classname\', index:\'classname\', width:150, sorttype:\"string\"},")
                context.write("{name:\'size\', index:\'size\', width:85, sorttype:\"int\"},")
                context.write("{name:\'username\', index:\'username\', width:150, sorttype:\"string\"},")
                context.write("{name:\'first_name\', index:\'first_name\', width:150, sorttype:\"string\", hidden:true},")
                context.write("{name:\'last_name\', index:\'last_name\', width:150, sorttype:\"string\", hidden:true},")
                context.write("{name:\'full_name\', index:\'last_name\', width:150, sorttype:\"string\"},")
                context.write("{name:\'view\', width:60, sortable:false, formatter:viewFormatter},")
                context.write("{name:\'register\', width:60, sortable:false, formatter:registerFormatter}")
            %>
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            if (iCol == 7) {
              var class_id = jQuery('#class_table').jqGrid('getCell', rowid, 0);
              location.href="/classes?class_id=" + class_id;
            } else if (iCol == 8) {
              <%
                if "user_id" in session:
                  context.write("var user_id = jQuery(\'#class_table\').jqGrid(\'getCell\', rowid, 9);")
                  context.write("if (user_id == \"\") {")
                  context.write("var class_id = jQuery(\'#class_table\').jqGrid(\'getCell\', rowid, 0);")
                  context.write("var username = jQuery(\'#class_table\').jqGrid(\'getCell\', rowid, 3);")
                  context.write("location.href=\"/register/classes/sign-up?class_id=\" + class_id + \"\";")
                  context.write("}")
                else:
                  context.write("var class_id = jQuery(\'#class_table\').jqGrid(\'getCell\', rowid, 0);")
                  context.write("var username = jQuery(\'#class_table\').jqGrid(\'getCell\', rowid, 3);")
                  context.write("location.href=\"/register/classes/sign-up?class_id=\" + class_id + \"\";")
              %>
            }
            return false;
          }, 
          jsonReader : {
            root: 'results',
            page: 'page',
            total: 'total',
            records: 'records',
            repeatitems: false,
            <%
              if "user_id" in session:
                context.write("id: \'cid\'")
              else:
                context.write("id: \'cid\'")
            %>
          },
          rowNum: 20,
          rowList: [20,40,60],
          pager: jQuery('#class_table_pager'),
          <%
            if "user_id" in session:
              context.write("sortname: \'cid\',")
            else:
              context.write("sortname: \'cid\',")
          %>
          viewrecords: true,
          sortorder: "asc",
          caption: "All Joinable Classes",
        });
        jQuery("#class_table").jqGrid('navGrid','#class_table_pager',{edit:false,add:false,del:false});
      }

      function viewFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>View</button>";
      }

      function registerFormatter(cellvalue, options, rowObject) {
        <%
          if "user_id" in session:
            context.write("var user_id = rowObject[\'user_id\'];")
            context.write("if (user_id == null) {")
            context.write("return \"<button ui-corner-all>Register</button>\";")
            context.write("}")
            context.write("return \"\";")
          else:
            context.write("return \"<button ui-corner-all>Register</button>\";")
        %>
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
