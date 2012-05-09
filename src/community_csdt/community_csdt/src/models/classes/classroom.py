import json
import logging

from community_csdt.src.models import database
from community_csdt.src.models.classes import class_comment, class_description, class_password
from community_csdt.src.utils import date

class Classroom(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Classroom.__getitem__()")
        log.debug("key = %s" % key)

        if key == "comments":
            return class_comment.ClassComment(self, key)
        elif key == "description":
            return class_description.ClassDescription(self, key)
        elif key == "password":
            return class_password.ClassPassword(self, key)

        raise KeyError

    # Returns the username for the owner (teacher) of the specified class. Classroom has to be active and public or privately viewable.
    def getClassOwner(self, class_id):
        log = logging.getLogger('csdt')
        log.info("Classroom.getClassOwner()")
    
        sql = "SELECT un.username AS username FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND un.user_id = u.id AND c.id = %s AND cm.permissions = 't' AND c.active = 1 AND u.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return
        
        return result["username"]

    # Returns the description and time of creation for a specific classroom. Classroom has to be active and public or privately viewable.
    def getClassDescription(self, class_id):
        log = logging.getLogger('csdt')
        log.info("Classroom.getClassDescription()")
   
        sql = "SELECT cn.classname AS classname, c.description AS description, c.time AS time FROM classnames cn, classrooms c WHERE c.id = cn.class_id AND c.id = %s AND c.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return

        class_info = {}
        date_obj = date.date()
        class_info["classname"] = result["classname"]
        class_info["description"] = result["description"]
        class_info["time"] = date_obj.modifyDate(result["time"])

        return class_info

    # Returns number of projects that are uploaded to a specific classroom, regardless of being public or privately viewable. Projects have to be active.
    def getNumOfProjectsForClass(self, class_id):
        log = logging.getLogger('csdt')
        log.info("Classroom.getNumOfProjectsForClass()")
  
        sql = "SELECT COUNT(id) AS num_projects FROM projects p, project_memberships pm WHERE pm.class_id = %s AND pm.project_id = p.id AND p.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")

        return result["num_projects"]

    # Returns a list of projects that are uploaded to a specific classroom, regardless of being public or privately viewable. Projects have to be active.
    def getAllProjectsForClass(self, class_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Classroom.getAllProjectsForClass()")

        sql = "SELECT table_A.proj_id AS id, table_A.username AS username, table_A.proj_name AS proj_name, table_A.proj_type AS proj_type, table_A.description AS description, table_A.num_views AS num_views, COUNT(table_B.rating) AS ratings, table_A.downloads AS downloads, table_A.stored_proj_name AS stored_proj_name, table_A.time AS time FROM (SELECT p.id AS proj_id, u.id AS user_id, un.username AS username, p.proj_name AS proj_name, p.proj_type AS proj_type, p.description AS description, p.num_views AS num_views, p.downloads AS downloads, p.stored_proj_name AS stored_proj_name, p.time AS time FROM projects p, project_memberships pm, users u, usernames un WHERE p.user_id = u.id AND u.id = un.user_id AND pm.project_id = p.id AND pm.class_id = %s AND p.active = 1) table_A LEFT JOIN (SELECT pr.project_id, pr.rating FROM project_ratings pr, users u WHERE u.id = pr.user_id AND u.active = 1) table_B ON table_B.project_id = table_A.proj_id GROUP BY table_A.proj_id ORDER BY %s %s;" % (str(class_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        proj_list = []
        for row in result:
            proj_hash = {}
            date_obj = date.date()
            proj_hash['id'] = row["id"]
            proj_hash['username'] = row["username"]
            proj_hash['proj_name'] = row["proj_name"]
            proj_hash['proj_type'] = row["proj_type"]
            proj_hash['description'] = row["description"]
            proj_hash['num_views'] = row["num_views"]
            proj_hash['ratings'] = row["ratings"]
            proj_hash['downloads'] = row["downloads"]
            proj_hash['stored_proj_name'] = row["stored_proj_name"]
            proj_hash['time'] = date_obj.modifyDate(row["time"])
            proj_list.append(proj_hash)
    
        return proj_list

    # Returns class name and a user's permissions given a user id and class id. Classroom has to be active and public or privately viewable.
    def determineClassPermissions(self, class_id, user_id):
        log = logging.getLogger('csdt')
        log.info("Classroom.getClassInformation()")
    
        sql = "SELECT cn.classname AS classname, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND c.id = %s AND u.id = %s AND c.active = 1 AND u.active = 1;" % (str(class_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return

        class_info = {}
        class_info["classname"] = result["classname"]
        class_info["permissions"] = result["permissions"]

        return class_info

    # Returns the number of students in a particular class. Classroom has to be active and public or privately viewable.
    def getIndividualClassSize(self, class_id):
        log = logging.getLogger('csdt')
        log.info("Classroom.getIndividualClassSize()")
 
        sql = "SELECT COUNT(DISTINCT cm.user_id) AS num_students FROM class_memberships cm, classnames cn, classrooms c, users u WHERE cm.permissions = \'s\' AND c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND cm.class_id = %s AND c.active = 1 AND u.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")

        return result["num_students"]

    # Returns a list of all students in a particular class. Classroom has to be active and public or privately viewable.
    def getAllPeopleInClass(self, class_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Classroom.getAllPeopleInClass()")
 
        sql = "SELECT un.username AS username, u.first_name AS first_name, u.last_name AS last_name, u.id AS user_id FROM class_memberships cm, classnames cn, classrooms c, usernames un, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND u.id = un.user_id AND cm.class_id = %s AND cm.permissions = 's' AND c.active = 1 AND u.active = 1 ORDER BY %s %s;" % (str(class_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['username'] = row["username"]
            class_hash['first_name'] = row["first_name"]
            class_hash['last_name'] = row["last_name"]
            class_hash['user_id'] = row["user_id"]
            class_hash['full_name'] = row["first_name"] + " " + row["last_name"]
            class_list.append(class_hash)
    
        return class_list

    # Verifies whether or not the given user_id exists in the database
    def verifyUserId(self, user_id):
        log = logging.getLogger('csdt')
        log.info("Classroom.verifyUserId()")
    
        sql = "SELECT id FROM users WHERE id = %s AND active = 1;" % (str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return

        return result["id"]

    # Sets the password flag to 1 so that a student user has permission to recover and change their password. Returns 0 if successful.
    def raisePasswordFlag(self, user_id): 
        log = logging.getLogger('csdt')
        log.info("Classroom.raisePasswordFlag()")

        # Sets password flag to 1 for the user
        sql = "UPDATE users SET reset_pass = 1 WHERE id = %s;" % (str(user_id))
        result = database.executeUpdateQuery(sql)

        return


