import json
import logging

from community_csdt.src.models import database

class AccountProject(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self.owner = self.__parent__.owner
        self.user_id = self.__parent__.user_id

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("AccountProject.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Verifies whether or not the project is under the jurisdiction of the user to moderate. Returns the project id if it is verified.
    def verifyProjectId(self, project_id, user_id):
        log = logging.getLogger('csdt')
        log.info("AccountProject.verifyProjectId()")
    
        sql = "SELECT p.id AS proj_id FROM projects p WHERE p.id = %s AND p.user_id = %s;" % (str(project_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("project is not under the jurisdication of the user")
            return

        return result["proj_id"]

    # Returns the number of classes that a single user is enrolled in (as a student and teacher). Class has to be active and public or privately viewable. 
    def getNumOfEnrolledClasses(self, user_id):
        log = logging.getLogger('csdt')
        log.info("AccountProject.getNumOfEnrolledClasses()")
      
        sql = "SELECT COUNT(DISTINCT cm.class_id) AS num_classes FROM class_memberships cm, classnames cn, classrooms c, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND cm.user_id = %s AND c.active = 1 AND u.active = 1;" % (str(user_id))
        result = database.executeSelectQuery(sql, "one")

        return result["num_classes"]

    # Returns list of all classes that a user is enrolled in (as a student and teacher) with whether or not the user uploaded a particular project to them 
    # Class has to be active and public or privately viewable. 
    def getAllEnrolledClassesWithUploadedProject(self, user_id, proj_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("AccountProject.getAllEnrolledClassesWithUploadedProject()")
   
        sql = "SELECT table_A.cid AS cid, table_A.classname AS classname, COUNT(table_B.project_id) AS uploaded FROM (SELECT c.id AS cid, cn.classname AS classname FROM class_memberships cm, classnames cn, classrooms c, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND cm.user_id = %s AND c.active = 1 AND u.active = 1) table_A LEFT JOIN (SELECT project_id, class_id FROM project_memberships WHERE project_id = %s) table_B ON table_B.class_id = table_A.cid GROUP BY table_A.cid ORDER BY %s %s;" % (str(user_id), str(proj_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["cid"]
            class_hash['classname'] = row["classname"]
            class_hash['uploaded'] = row["uploaded"]
            class_list.append(class_hash)
    
        return class_list

    # Verifies whether or not the user is a participant in the class. Classroom has to be active and public or privately viewable.
    def verifyUserAsClassParticipant(self, class_id, user_id):
        log = logging.getLogger('csdt')
        log.info("AccountProject.verifyUserAsClassParticipant()")
    
        sql = "SELECT c.id AS class_id FROM class_memberships cm, classrooms c, users u WHERE cm.class_id = c.id AND cm.user_id = u.id AND c.id = %s AND u.id = %s AND c.active = 1 AND u.active = 1;" % (str(class_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user is not a participant in the class")
            return
        
        return result["class_id"]

    # Copies project to a particular class
    def copyProjectToClass(self, proj_id, class_id): 
        log = logging.getLogger('csdt')
        log.info("AccountProject.copyProjectToClass()")
    
        # Adds the class that the project will be associated with
        sql = "INSERT INTO project_memberships (project_id, class_id) VALUES (%s, %s);" % (str(proj_id), str(class_id))
        result = database.executeInsertQuery(sql)

        return 

    # Removes project from a particular class
    def removeProjectFromClass(self, proj_id, class_id): 
        log = logging.getLogger('csdt')
        log.info("AccountProject.removeProjectFromClass()")
    
        # Deletes the class that the project will be associated with
        sql = "DELETE FROM project_memberships WHERE project_id = %s AND class_id = %s;" % (str(proj_id), str(class_id))
        result = database.executeDeleteQuery(sql)

        return 


