<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Manage Classes</title>
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div class="article">
    <h2>Managing Classes</h2>
    <div class="clr"></div>
    <table id="class_table" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="class_table_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#class_table").jqGrid({
          url: '${path_url}-tables',
          datatype: "json",
          mtype: 'GET',
          colNames:['CID', 'Classname', '# Students', 'View Class', 'Delete Class'],
          colModel:[
            {name:'cid', index:'cid', width:25, sorttype:"int", hidden:true},
            {name:'classname', index:'classname', width:200, sorttype:"string"},
            {name:'size', index:'size', width:85, sorttype:"int"},
            {name:'view', width:80, sortable:false, formatter:viewFormatter},
            {name:'delete', width:80, sortable:false, formatter:deleteFormatter}
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            if (iCol == 3) {
              var class_id = jQuery('#class_table').jqGrid('getCell', rowid, 0);
              location.href="/classes?class_id=" + class_id;
            } else if (iCol == 4) {
              var class_id = jQuery('#class_table').jqGrid('getCell', rowid, 0);
              location.href="/";
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
          caption: "Managing Classes",
        });
        jQuery("#class_table").jqGrid('navGrid','#class_table_pager',{edit:false,add:false,del:false});
      }

      function viewFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>View</button>";
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
