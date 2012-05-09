<%inherit file="base.html"/>

<%block name="title">
  <title>CSDT Community | Uploaded</title>
</%block>

<%block name="info">
<div class="content content_resize_main body-sticky-footer mainbar">
  <%
    if success == 1:
      context.write("<h2>File Uploaded Successfully.</h2>")
    else:
      context.write("<h2>Problem with File.</h2>")
      content.write("<p>Sorry for the inconvience, but we could not upload the file.</p>")
  %>
  <p><a href="/">Click here to return to home page</a></p>
  <div class="sidebar"></div>
  <div class="clr"></div>
</div>
</%block>
