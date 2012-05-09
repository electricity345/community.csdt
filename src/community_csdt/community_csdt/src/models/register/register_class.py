import json
import logging

from community_csdt.src.models import database
from community_csdt.src.utils import date

class RegisterClass(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.__getitem__()")
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

    # Returns the number of classes that are available for a user to join. Classrooms have to be active. (Visible?)
    def getNumOfRegistableClasses(self):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.getNumOfRegistableClasses()")

        sql = "SELECT COUNT(DISTINCT cm.class_id) AS num_classes FROM class_memberships cm, classnames cn, classrooms c, users u WHERE cm.permissions = 't' AND c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND c.active = 1 AND u.active = 1;"
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("no classes exist")
            return

        return result["num_classes"]

    # Returns a list of all classrooms that are available for a user to join. Classroom has to be active. (Visible?)
    def getAllRegistableClasses(self, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.getAllRegistableClasses()")

        sql = "SELECT table_B.class_id AS cid, table_B.classname AS classname, COUNT(cm.user_id) AS size, table_B.username AS username, table_B.first_name AS first_name, table_B.last_name AS last_name FROM (SELECT table_A.class_id AS class_id, table_A.classname AS classname, table_A.username AS username, table_A.first_name AS first_name, table_A.last_name AS last_name, cm.user_id AS user_id, table_A.permissions AS permissions FROM (SELECT cn.class_id AS class_id, cn.classname AS classname, un.username AS username, u.first_name AS first_name, u.last_name AS last_name, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE cm.permissions = 't' AND c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND u.id = un.user_id AND c.active = 1 AND u.active = 1) table_A, class_memberships cm, users u WHERE u.active = 1 AND table_A.class_id = cm.class_id AND cm.user_id = u.id) table_B LEFT JOIN class_memberships cm ON table_B.class_id = cm.class_id AND table_B.permissions <> cm.permissions AND table_B.user_id = cm.user_id GROUP BY table_B.class_id ORDER BY %s %s;" % (sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["cid"]
            class_hash['classname'] = row["classname"]
            class_hash['size'] = row["size"]
            class_hash['username'] = row["username"]
            class_hash['first_name'] = row["first_name"]
            class_hash['last_name'] = row["last_name"]
            class_hash['full_name'] = class_hash['first_name'] + " " + class_hash['last_name']
            class_list.append(class_hash)
    
        return class_list

    # Returns a list of all classrooms that are available for a user to join. Classroom has to be active. (Visible?)
    def getAllRegistableClassesForAUser(self, user_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.getAllRegistableClassesForAUser()")

        sql = "SELECT table_C.class_id AS cid, table_C.classname AS classname, COUNT(cm.user_id) AS size, table_C.username AS username, table_C.first_name AS first_name, table_C.last_name AS last_name, table_C.own_user_id AS user_id FROM (SELECT table_B.class_id AS class_id, table_B.classname AS classname, table_B.username AS username, table_B.first_name AS first_name, table_B.last_name AS last_name, table_B.user_id AS own_user_id, cm.user_id AS user_id, table_B.permissions AS permissions FROM (SELECT table_A.class_id AS class_id, table_A.classname AS classname, table_A.username AS username, table_A.first_name AS first_name, table_A.last_name AS last_name, table_A.permissions AS permissions, cm.user_id AS user_id FROM (SELECT cn.class_id AS class_id, cn.classname AS classname, un.username AS username, u.first_name AS first_name, u.last_name AS last_name, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE cm.permissions = 't' AND c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND u.id = un.user_id AND c.active = 1 AND u.active = 1) table_A LEFT JOIN class_memberships cm ON table_A.class_id = cm.class_id AND cm.user_id = %s) table_B, class_memberships cm, users u WHERE u.active = 1 AND table_B.class_id = cm.class_id AND cm.user_id = u.id) table_C LEFT JOIN class_memberships cm ON table_C.class_id = cm.class_id AND table_C.permissions <> cm.permissions AND table_C.user_id = cm.user_id GROUP BY table_C.class_id ORDER BY %s %s;" % (str(user_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["cid"]
            class_hash['classname'] = row["classname"]
            class_hash['size'] = row["size"]
            class_hash['username'] = row["username"]
            class_hash['first_name'] = row["first_name"]
            class_hash['last_name'] = row["last_name"]
            class_hash['user_id'] = row["user_id"]
            class_hash['full_name'] = class_hash['first_name'] + " " + class_hash['last_name']
            class_list.append(class_hash)
    
        return class_list

    # Checks whether or not the queried password matches the class password's. Classroom has to be active. 
    def verifyClassPassword(self, class_id, password):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.verifyClassPassword()")

        sql = "SELECT c.id AS class_id FROM classnames cn, classrooms c WHERE c.id = cn.class_id AND c.id = %s AND cn.pass = '%s' AND c.active = 1;" % (str(class_id), str(password))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return

        return result["class_id"]

    # Registers a user as a student of a particular class
    def registerClass(self, user_id, class_id):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.registerClass()")

        # Creates an association as a student of a particular class
        sql = "INSERT INTO class_memberships (user_id, class_id, permissions) VALUES (%s, %s, '%s');" % (str(user_id), str(class_id), 's')
        result = database.executeInsertQuery(sql)
        
        return

    # Checks if classname already exists in database and is currently active. Classroom has to be active and public or privately viewable.
    # Returns none if classname is unique
    def doesClassnameExist(self, classname):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.doesClassnameExist()")

        sql = "SELECT c.id AS class_id FROM classnames cn, classrooms c WHERE c.id = cn.class_id AND cn.classname = '%s' AND c.active = 1;" % (str(classname))
        result = database.executeSelectQuery(sql, "one")
        if result is not None:
            log.warning("class already exists")
            return result["class_id"]

        return

    # Creates a class for a specific user. Returns the class_id of the newly created class.
    def createClass(self, user_id, classname, password, level):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.createClass()")

        # Creates a classroom
        sql = "INSERT INTO classrooms (owner, description, flag_comment_level) VALUES (%s, '%s', %s);" % (str(user_id), "", str(level))
        class_id = database.executeInsertQuery(sql)
        log.debug("class_id = %s" % class_id)

        # Creates a classname
        sql = "INSERT INTO classnames (class_id, classname, pass) VALUES (%s, '%s', '%s');" % (str(class_id), str(classname), str(password))        
        result = database.executeInsertQuery(sql)

        # Creates an association between the user who created the class and the class itself
        sql = "INSERT INTO class_memberships (user_id, class_id, permissions) VALUES (%s, %s, '%s');" % (str(user_id), str(class_id), 't')
        result = database.executeInsertQuery(sql)

        return class_id

    # Determines if a user is apart of a particular class as either a teacher or student
    def isUserApartOfClass(self, user_id, class_id):
        log = logging.getLogger('csdt')
        log.info("RegisterClass.isUserApartOfClass()")

        # Creates an association as a student of a particular class
        sql = "SELECT class_id FROM class_memberships WHERE user_id = %s AND class_id = %s;" % (str(user_id), str(class_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user is not apart of the particular class")
            return

        return result["class_id"]


