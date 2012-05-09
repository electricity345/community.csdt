<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Flagged Comment Users</title>
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div class="article">
    <h2>Flagged Comment Users</h2>
    <div class="clr"></div>
    <table id="flagged_comment_users" class="table-center" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="flagged_comment_users_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#flagged_comment_users").jqGrid({
          url: '${path_url}-flag-tables?comment_id=${comment_id}',
          datatype: "json",
          mtype: 'GET',
          colNames:['Key', 'Flagged Users', 'View Projects', 'View Profile'],
          colModel:[
            {name:'key', width:25, key:true, hidden:true},
            {name:'username', index:'username', width:200, sorttype:"string"},
            {name:'projects', width:80, sortable:false, formatter:projectFormatter},
            {name:'view', width:80, sortable:false, formatter:profileFormatter},
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            if (iCol == 2) {
              var username = jQuery('#flagged_comment_users').jqGrid('getCell', rowid, 1);
              location.href="/accounts/" + username + "/projects";
            } else if (iCol == 3) {
              var username = jQuery('#flagged_comment_users').jqGrid('getCell', rowid, 1);
              location.href="/accounts/" + username;
            } 
            return false;
          }, 
          jsonReader : {
            root: 'results',
            page: 'page',
            total: 'total',
            records: 'records',
            repeatitems: false,
            id: 'id'
          },
          rowNum: 20,
          rowList: [20,40,60],
          pager: jQuery('#flagged_comment_users_pager'),
          sortname: 'u.username',
          viewrecords: true,
          sortorder: "asc",
          caption: "Flagged Comments",
        });
        jQuery("#flagged_comment_users").jqGrid('navGrid','#flagged_comment_users_pager',{edit:false,add:false,del:false});
      }

      function projectFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Projects</button>";
      }

      function profileFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Profiles</button>";
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
