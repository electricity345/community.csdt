import json
import logging
import os
import re

from BeautifulSoup import BeautifulStoneSoup
from mako.template import Template
from mako.runtime import Context

from community_csdt.src.models import database

class Upload(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Upload.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Adds a new project to the database
    def addProject(self, user_id, proj_name, description, visible):
        log = logging.getLogger('csdt')
        log.debug("Upload.addProject()")
    
        # Stores details of the project
        sql = "INSERT INTO projects (user_id, proj_name, stored_proj_name, proj_type, description, visible) VALUES (%s, '%s', '%s', '%s', '%s', %s);" % (str(user_id), str(proj_name), "", "", str(description), str(visible))
        project_id = database.executeInsertQuery(sql)
        log.debug("project_id = %s" % project_id)

        return project_id   

    # Finds the codename and version tag within the xml file. Returns the codename and version of the project if found. Otherwise, returns an empty list
    def findProjectInformation(self, textfile):
        log = logging.getLogger('csdt')
        log.info("Upload.findProjectInformation()")

        xml_file = open(textfile, "r")
        xml = xml_file.read()

        soup = BeautifulStoneSoup(xml)
        engine_tag = soup.find('project', attrs={"codename":re.compile("^\S+$"), "version":re.compile("^\S+$")})

        engine_value = []
        if (engine_tag == None):
            log.debug("no tags found")
        else:
            log.debug("codename = %s" % engine_tag["codename"])
            log.debug("version = %s" % engine_tag["version"])
            engine_value.append(engine_tag["codename"])
            engine_value.append(engine_tag["version"])

        return engine_value

    # Adds the stored project name and project type to a given project id
    def updateProject(self, proj_id, filename, proj_type):
        log = logging.getLogger('csdt')
        log.debug("Upload.updateProject()")
    
        sql = "UPDATE projects SET stored_proj_name = '%s', proj_type = '%s' WHERE id = %s;" % (str(filename), str(proj_type), str(proj_id))
        result = database.executeUpdateQuery(sql)

        return    

    # Creates a corresponding JNLP file for a given xml file.
    def createJNLP(self, host_url, proj_type, stored_proj_name, version, xml_filename):
        log = logging.getLogger('csdt')
        log.info("Upload.createJNLP()")

        jnlp_filename = stored_proj_name + ".jnlp"
        log.debug("jnlp filename = %s" % jnlp_filename)

        stored_proj_name = stored_proj_name.replace(" ", "%20")
        escaped_jnlp_filename = stored_proj_name + ".jnlp"
        log.debug("escaped jnlp filename = %s" % jnlp_filename)

        # Path = ../../../uploads/projects/PROJ_TYPE/jnlp/FILENAME
        jnlp_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'uploads', 'projects', proj_type.upper(), 'jnlp', jnlp_filename)

        jnlp_path = host_url + "/uploads/projects/" + proj_type.upper() + "/jnlp/" + escaped_jnlp_filename
        xml_path = host_url + "/uploads/projects/" + proj_type.upper() + "/xml/" + xml_filename

        temp_jnlp_filename = proj_type.lower() + ".v" + version.lower() + ".jnlp"
        log.debug("temp_jnlp_filename = %s" % temp_jnlp_filename)

        # Path = ../../../uploads/projects/PROJ_TYPE/templates/FILENAME
        temp_jnlp_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'uploads', 'projects', proj_type.upper(), 'templates', temp_jnlp_filename)

        # Checks if a template jnlp file exists for a specific project. If so, it creates a jnlp file for that specific project.
        try:
            proj_jnlp_file = open(temp_jnlp_file_path, "r")
            tpl_xml = proj_jnlp_file.read()
            log.debug("tpl_xml = %s" % tpl_xml)
            tpl = Template(tpl_xml)
            with open(jnlp_file_path, 'w') as f:
                ctx = Context(f, data=xrange(10000000), jnlp=jnlp_path, xml=xml_path)
                tpl.render_context(ctx) 
        except IOError:
            log.warning("project is not supported")
            return 0
            
        log.debug("successfully created JNLP file")
        return 1


