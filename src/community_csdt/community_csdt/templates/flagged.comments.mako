<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | ${owner} | Flagged Comments</title>
</%block>

<%block name="scripts">
  $(document).ready(function(){
    $("#approve-comment-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#ban-comment-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });
  });
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <div id="approve-comment-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully approved the comment.
    </p>
  </div>
  <div id="ban-comment-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully banned the comment.
    </p>
  </div>

  <div class="article">
    <h2>Flagged Comments</h2>
    <div class="clr"></div>
    <table id="flagged_comments" class="table-center" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="flagged_comments_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#flagged_comments").jqGrid({
          url: '${path_url}-tables',
          datatype: "json",
          mtype: 'GET',
          colNames:['Key', 'PCID' ,'Comment Owner', 'Project Name', 'Text', 'Time', 'Flagged Users', 'Accept', 'Ban'],
          colModel:[
            {name:'key', width:25, key:true, hidden:true},
            {name:'proj_comment_id', index:'proj_comment_id', width:25, sorttype:"int", hidden:true},
            {name:'comment_owner', index:'comment_owner', width:120, sorttype:"string"},
            {name:'proj_name', index:'proj_name', width:100, sorttype:"string", hidden:true},
            {name:'text', index:'text', width:250, sorttype:"string"},
            {name:'time', index:'time', width:100, sorttype:"string"},
            {name:'flag_users', width:90, sortable:false, formatter:flagUsersFormatter},
            {name:'accept', width:50, sortable:false, formatter:acceptFormatter},
            {name:'ban', width:50, sortable:false, formatter:banFormatter}
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            if (iCol == 6) {
              var proj_comment_id = jQuery('#flagged_comments').jqGrid('getCell', rowid, 1);
              location.href="/accounts/${owner}/admin/comments/users-list?comment_id=" + proj_comment_id;
            } else if (iCol == 7) {
              var proj_comment_id = jQuery('#flagged_comments').jqGrid('getCell', rowid, 1);
              $.ajax({
                type: "POST",
                url: "/accounts/${owner}/admin/comments/approve?comment_id=" + proj_comment_id,
                success: function(result) {
                  var obj = jQuery.parseJSON(result);
                  if (obj.result == 0) {
                    $("#approve-comment-success").dialog("open");
                  } 
                },
                error: function(jqXHR, textStatus, errorThrown) {
                  alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
                  location.href = "/";
                }
              });
            } else if (iCol == 8) {
              var proj_comment_id = jQuery('#flagged_comments').jqGrid('getCell', rowid, 1);
              $.ajax({
                type: "POST",
                url: "/accounts/${owner}/admin/comments/ban?comment_id=" + proj_comment_id,
                success: function(result) {
                  var obj = jQuery.parseJSON(result);
                  if (obj.result == 0) {
                    $("#ban-comment-success").dialog("open");
                  } 
                },
                error: function(jqXHR, textStatus, errorThrown) {
                  alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
                  location.href = "/";
                }
              });
            }
            return false;
          }, 
          jsonReader : {
            root: 'results',
            page: 'page',
            total: 'total',
            records: 'records',
            repeatitems: false,
            id: 'proj_comment_id'
          },
          rowNum: 20,
          rowList: [20,40,60],
          pager: jQuery('#flagged_comments_pager'),
          sortname: 'time',
          viewrecords: true,
          sortorder: "asc",
          caption: "Flagged Comments",
        });
        jQuery("#flagged_comments").jqGrid('navGrid','#flagged_comments_pager',{edit:false,add:false,del:false});
      }

      function flagUsersFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>List</button>";
      }

      function acceptFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Accept</button>";
      }

      function banFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>Ban</button>";
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
