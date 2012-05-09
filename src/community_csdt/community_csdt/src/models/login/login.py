import json
import logging

from community_csdt.src.models import database

class Login(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Login.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Checks user credentials. Returns user id if user authentication is successful.
    def authenticateUser(self, username, password):
        log = logging.getLogger('csdt')
        log.info("Login.authenticateUser()")

        sql = "SELECT un.user_id AS user_id FROM usernames un, users u WHERE un.user_id = u.id AND un.username = '%s' AND un.pass = '%s' AND u.active = 1;" % (str(username), str(password))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return

        return result["user_id"]

    # Returns the username, first name, last name, email, and about me information of a user given their user_id
    def getUserProfileInformation(self, user_id):
        log = logging.getLogger('csdt')
        log.info("Login.getUserProfileInformation()")
    
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

    # Returns a list of all classrooms that a single user (teacher) manages. Classrooms have to be active and public or privately viewable.
    def getAllClassesEnrolledAsTeacher(self, user_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Login.getAllClassesEnrolledAsTeacher()")

        sql = "SELECT table_B.class_id AS class_id, table_B.classname AS classname, COUNT(cm.user_id) AS size FROM (SELECT table_A.class_id AS class_id, table_A.classname AS classname, cm.user_id AS user_id, table_A.permissions AS permissions FROM (SELECT cn.class_id AS class_id, cn.classname AS classname, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND cm.user_id = %s AND cm.permissions = 't' AND c.active = 1 AND u.active = 1) table_A, class_memberships cm, users u WHERE u.active = 1 AND table_A.class_id = cm.class_id AND cm.user_id = u.id) table_B LEFT JOIN class_memberships cm ON table_B.class_id = cm.class_id AND table_B.permissions <> cm.permissions AND table_B.user_id = cm.user_id GROUP BY table_B.class_id ORDER BY %s %s;" % (str(user_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")
        if result is None:
            log.warning("teacher does not exist")
            return

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["class_id"]
            class_hash['classname'] = row["classname"]
            class_hash['size'] = row["size"]           
            class_list.append(class_hash)

        return class_list

    # Returns a list of all classrooms that a single user is enrolled in. Classrooms have to be active and public or privately viewable. 
    def getAllClassesEnrolledAsStudent(self, user_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Login.getAllClassesEnrolledAsStudent()")

        sql = "SELECT table_B.class_id AS class_id, table_B.classname AS classname, COUNT(cm.user_id) AS size, table_B.username AS username, table_B.first_name AS first_name, table_B.last_name AS last_name FROM (SELECT table_A.class_id AS class_id, table_A.classname AS classname, un.username AS username, u.first_name AS first_name, u.last_name AS last_name, cm.user_id AS user_id, table_A.permissions AS own_permissions FROM (SELECT cn.class_id AS class_id, cn.classname AS classname, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND cm.user_id = %s AND cm.permissions = 's' AND c.active = 1 AND u.active = 1) table_A, class_memberships cm, usernames un, users u WHERE table_A.class_id = cm.class_id AND cm.user_id = u.id AND u.id = un.user_id AND u.active = 1) table_B LEFT JOIN class_memberships cm ON table_B.class_id = cm.class_id AND table_B.own_permissions = cm.permissions AND table_B.user_id = cm.user_id GROUP BY table_B.class_id ORDER BY %s %s;" % (str(user_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")
        if result is None:
            log.warning("user does not exist")
            return

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["class_id"]
            class_hash['classname'] = row["classname"]
            class_hash['size'] = row["size"]
            class_hash['username'] = row["username"]
            class_hash['first_name'] = row["first_name"]
            class_hash['last_name'] = row["last_name"]
            class_hash['full_name'] = class_hash["first_name"] + " " + class_hash["last_name"]
            class_list.append(class_hash)

        return class_list


