<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | ${owner} | Copy Project to Class</title>
</%block>

<%block name="scripts">
  $(document).ready(function(){
    $("#copy-to-class-success").dialog({
      autoOpen: false,
      modal: true,
      buttons: {
        "Ok": function() { 
          location.href = "${full_url}";
          $(this).dialog("close"); 
        }
      }
    });

    $("#remove-from-class-success").dialog({
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
  <div id="copy-to-class-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully copied the project to the class.
    </p>
  </div>
  <div id="remove-from-class-success" title="Warning">
    <p>
      <span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 50px 0;"></span> 
      You have successfully removed the project from the class.
    </p>
  </div>

  <div class="article">
    <h2>Classes Enrolled In</h2>
    <div class="clr"></div>
    <table id="class_table" class="scroll" cellpadding="0" cellspacing="0" > </table>
    <div id="class_table_pager" class="scroll" style="text-align:center;"> </div>

    <script type="text/javascript"> 
      function jqinvoke() {
        jQuery("#class_table").jqGrid({
          url: '${path_url}-tables?proj_id=${proj_id}',
          datatype: "json",
          mtype: 'GET',
          colNames:['CID', 'Classname', 'View Class', "Upload to Class"],
          colModel:[
            {name:'cid', index:'cid', width:25, sorttype:"int", hidden:true},
            {name:'classname', index:'classname', width:300, sorttype:"string"},
            {name:'view', width:75, sortable:false, formatter:viewFormatter},
            {name:'uploaded', width:90, sortable:false, editable:true, edittype:"checkbox", editoptions:{value:"1:0"}, formatter:'checkbox', formatoptions:{disabled:false}},
          ],
          onCellSelect: function(rowid, iCol, cellcontent, e) {
            if (iCol == 2) {
              var class_id = jQuery('#class_table').jqGrid('getCell', rowid, 0);
              location.href="/classes?class_id=" + class_id;
            } 

            return false;
          },
          loadComplete : function() {
            jQuery(".jqgrow td input").each(function () {
              jQuery(this).click(function (e) {
                // e.target point to <input> DOM element
                var tr = $(e.target).closest('tr');
                var class_id = tr[0].id
                var value = $(e.target).is(':checked')

                /* Adds or removes association between a project and a particular class */
                if (value) {
                  $.ajax({
                    type: "POST",
                    url: "/accounts/${owner}/admin/projects/copy-to-class?proj_id=${proj_id}&class_id=" + class_id,
                    success: function(result) {
                      var obj = jQuery.parseJSON(result);
                      if (obj.result == 0) {
                        $("#copy-to-class-success").dialog("open");
                      } 
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                      alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
                      location.href = "/";
                    }
                  });
                } else {
                  $.ajax({
                    type: "POST",
                    url: "/accounts/${owner}/admin/projects/remove-from-class?proj_id=${proj_id}&class_id=" + class_id,
                    success: function(result) {
                      var obj = jQuery.parseJSON(result);
                      if (obj.result == 0) {
                        $("#remove-from-class-success").dialog("open");
                      } 
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                      alert("Fail - Code: " + jqXHR + " textStatus: " + textStatus + " error thrown: " + errorThrown);
                      location.href = "/";
                    }
                  });
                }

              });
            });
          }, 
          jsonReader : {
            root: 'results',
            page: 'page',
            total: 'total',
            records: 'records',
            repeatitems: false,
            id: 'cid'
          },
          rowNum: 20,
          rowList: [20,40,60],
          pager: jQuery('#class_table_pager'),
          sortname: 'classname',
          viewrecords: true,
          sortorder: "asc",
          caption: "Classes Enrolled In",
        });
        jQuery("#class_table").jqGrid('navGrid','#class_table_pager',{edit:false,add:false,del:false});
      }

      function viewFormatter(cellvalue, options, rowObject) {
        return "<button ui-corner-all>View</button>";
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
