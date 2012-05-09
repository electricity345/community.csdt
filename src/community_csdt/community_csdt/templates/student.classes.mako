<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | ${owner} | Classes Joined</title>
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div class="article">
    <h2>Classes Enrolled In</h2>
    <div class="clr"></div>
    <table id="class_table" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="class_table_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#class_table").jqGrid({
          url: '${path_url}-tables',
          datatype: "json",
          mtype: 'GET',
          colNames:['CID', 'Classname', '# Students', 'Owner Username', 'Owner First Name', 'Owner Last Name', 'Owner Name', 'View Class'],
          colModel:[
            {name:'cid', index:'cid', width:25, sorttype:"int", hidden:true},
            {name:'classname', index:'classname', width:150, sorttype:"string"},
            {name:'size', index:'size', width:85, sorttype:"int"},
            {name:'username', index:'username', width:150, sorttype:"string"},
            {name:'first_name', index:'first_name', width:150, sorttype:"string", hidden:true},
            {name:'last_name', index:'last_name', width:150, sorttype:"string", hidden:true},
            {name:'full_name', index:'last_name', width:150, sorttype:"string"},
            {name:'view', width:60, sortable:false, formatter:viewFormatter},
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            if (iCol == 7) {
              var class_id = jQuery('#class_table').jqGrid('getCell', rowid, 0);
              location.href="/classes?class_id=" + class_id;
            } 
            return false;
          }, 
          jsonReader : {
            root: 'results',
            page: 'page',
            total: 'total',
            records: 'records',
            repeatitems: false,
            id: 'table_B.class_id'
          },
          rowNum: 20,
          rowList: [20,40,60],
          pager: jQuery('#class_table_pager'),
          sortname: 'table_B.class_id',
          viewrecords: true,
          sortorder: "asc",
          caption: "Classes Enrolled In",
        });
        jQuery("#class_table").jqGrid('navGrid','#class_table_pager',{edit:false,add:false,del:false});
      }

      function viewFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>View</button>";
      }

      function registerFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Register</button>";
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
