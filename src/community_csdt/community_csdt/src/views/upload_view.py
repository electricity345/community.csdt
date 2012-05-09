import json
import logging
import os

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.upload import *

class UploadView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Only logged in users can access the particular web page
    def userOnlyAuthorization(self, session):
        log = logging.getLogger('csdt')
        log.info("upload_view.ownerOnlyAuthorization()")

        # Verifies that only logged in users can perform the following task (Authorization)
        if "user_id" not in session or "username" not in session:
            log.warning("user_id is not in session or username is not in session")
            raise HTTPForbidden()

        return

    # Resource url = "/upload" - Processes the upload file and displays the successful upload page after completion
    @view_config(context='community_csdt.src.models.upload.upload.Upload', name='', renderer='uploaded.mako')
    def uploadXML(self):
        log = logging.getLogger('csdt')
        log.info("upload_view.uploadXML()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("content type = %s" % self.request.content_type)

        if "upload_file" not in self.request.params or "upload_name" not in self.request.params or "upload_description" not in self.request.params or "upload_visibility" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()   

        self.userOnlyAuthorization(session)

        upload_file = self.request.params["upload_file"]
        proj_name = self.request.params["upload_name"]    
        description = self.request.params["upload_description"]
        visibility = self.request.params["upload_visibility"] 
   
        if upload_file.type != "text/xml":
            log.warning("Invalid File - File is not an xml file")
            raise HTTPBadRequest()
 
        log.debug("visibility = %s" % visibility)
        log.debug("upload file - content type = %s" % upload_file.type)
        log.debug("type of upload file = %s" % type(upload_file))
        log.debug("original filename = %s" % upload_file.filename)
        log.debug("size = %s" % len(upload_file.value))

        # Appends the project id to the front of the desired project name
        proj_id = self.context.addProject(session["user_id"], proj_name, description, visibility)
        stored_proj_name = str(proj_id) + "." + str(proj_name)
        xml_filename = stored_proj_name + ".xml"
        log.debug("new xml filename = %s" % xml_filename)

        # Path = ../../uploads/tmp/FILENAME
        xml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', 'tmp', xml_filename)
        log.debug("Trying to open: %s" % xml_path)

        new_file = open(xml_path, "w")
        new_file.write(upload_file.file.read()) 
        new_file.close()

        # Gets the project type and version number for the project if it is there. Otherwise, it removes the file and returns a failure result.
        engine_value = self.context.findProjectInformation(xml_path)
        if not engine_value:
            log.warning("Corrupt XML File - We can't process the XML file")
            try:
                new_file = open(xml_path)
                os.unlink(xml_path)
                new_file.close()
            except IOError:
                pass

            return {'session':session, 'success':-1}  

        proj_type = engine_value[0]
        version = engine_value[1]
        log.debug("project type = %s" % proj_type)
        log.debug("version = %s" % version)

        user_id = session["user_id"]
        self.context.updateProject(proj_id, stored_proj_name, proj_type)

        # Path = ../../uploads/projects/PROJ_TYPE/xml/FILENAME
        new_xml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', 'projects', proj_type.upper(), 'xml', xml_filename)
        os.rename(xml_path, new_xml_path) # Moves xml file from tmp folder to proj_type folder
        success = self.context.createJNLP(self.request.host_url, proj_type, stored_proj_name, version, xml_filename)

        return {'session':session, 'success':success}


