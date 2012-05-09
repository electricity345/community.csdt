import json
import logging

from community_csdt.src.models import database
from community_csdt.src.utils import date

class RegisterStudent(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("RegisterStudent.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Returns the username for the owner (teacher) of the specified class. Classroom has to be active and public or privately viewable.
    def getClassOwner(self, class_id):
        log = logging.getLogger('csdt')
        log.info("RegisterStudent.getClassOwner()")
    
        sql = "SELECT un.username AS username FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND un.user_id = u.id AND c.id = %s AND cm.permissions = \'t\' AND c.active = 1 AND u.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return
        
        return result["username"]

    # Returns the description and time of creation for a specific classroom. Classroom has to be active and public or privately viewable.
    def getClassDescription(self, class_id):
        log = logging.getLogger('csdt')
        log.info("RegisterStudent.getClassDescription()")
   
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

    # Checks if username already exists in database and is currently active.
    def doesUsernameExist(self, username):
        log = logging.getLogger('csdt')
        log.info("RegisterStudent.doesUsernameExist()")
  
        sql = "SELECT un.user_id AS user_id FROM usernames un, users u WHERE un.user_id = u.id AND un.username = \'%s\' AND u.active = 1;" % (str(username))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return
        
        return result["user_id"]

    # Creates a student account for users who only register with a class. They do not need to provide an email address.
    def createStudentAccount(self, first_name, last_name, username, password, class_id):
        log = logging.getLogger('csdt')
        log.info("RegisterStudent.createStudentAccount()")

        # Creates a user - without an email address and permissions of a student (s)  
        sql = "INSERT INTO users (first_name, last_name, permissions) VALUES ('%s', '%s', '%s');" % (str(first_name), str(last_name), 's')
        user_id = database.executeInsertQuery(sql)
        log.debug("user_id = %s" % user_id)
        
        # Creates a username
        sql = "INSERT INTO usernames (user_id, username, pass) VALUES (%s, '%s', '%s');" % (str(user_id), str(username), str(password))
        result = database.executeInsertQuery(sql)

        # Creates a user profile entry
        sql = "INSERT INTO user_profile (user_id, about) VALUES (%s, '%s');" % (str(user_id), '')
        result = database.executeInsertQuery(sql)

        # Creates an association as a student of a particular class
        sql = "INSERT INTO class_memberships (user_id, class_id, permissions) VALUES (%s, %s, '%s');" % (str(user_id), str(class_id), 's')
        result = database.executeInsertQuery(sql)

        return user_id

    # Returns the username, first name, last name, email, and about me information of a user given their user_id
    def getUserProfileInformation(self, user_id):
        log = logging.getLogger('csdt')
        log.info("RegisterStudent.getUserProfileInformation()")
    
        sql = "SELECT un.username AS username, u.first_name AS first_name, u.last_name AS last_name, u.email AS email, u.permissions AS permissions, u.reset_pass AS reset_pass, u.reset_pass_counter AS reset_pass_counter, up.about AS about FROM usernames un, user_profile up, users u WHERE u.id = %s AND u.id = un.user_id AND u.id = up.user_id AND u.active = 1;" % (str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return

        user_info = {}
        user_info["username"] = result["username"]
        user_info["first_name"] = result["first_name"]
        user_info["last_name"] = result["last_name"]
        user_info["email"] = result["email"]
        user_info["permissions"] = result["permissions"]
        user_info["reset_pass"] = result["reset_pass"]
        user_info["reset_pass_counter"] = result["reset_pass_counter"]
        user_info["about"] = result["about"]

        return user_info


