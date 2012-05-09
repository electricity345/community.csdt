import json
import logging

from community_csdt.src.models import database

class ClassPassword(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("ClassPassword.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Returns the username for the owner (teacher) of the specified class. Classroom has to be active and public or privately viewable.
    def getClassOwner(self, class_id):
        log = logging.getLogger('csdt')
        log.info("ClassPassword.getClassOwner()")
    
        sql = "SELECT un.username AS username FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND un.user_id = u.id AND c.id = %s AND cm.permissions = 't' AND c.active = 1 AND u.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return
        
        return result["username"]

    # Checks whether or not the queried password matches the class password's. Classroom has to be active. 
    def verifyClassPassword(self, class_id, password):
        log = logging.getLogger('csdt')
        log.info("ClassPassword.verifyClassPassword()")

        sql = "SELECT c.id AS class_id FROM classnames cn, classrooms c WHERE c.id = cn.class_id AND c.id = %s AND cn.pass = '%s' AND c.active = 1;" % (str(class_id), str(password))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return

        return result["class_id"]

    # Changes the password of a class
    def changeClassPassword(self, class_id, password): 
        log = logging.getLogger('csdt')
        log.info("ClassPassword.changeClassPassword()")
 
        # Changes the password for the class
        sql = "UPDATE classnames SET pass = '%s' WHERE class_id = %s;" % (str(password), str(class_id))
        result = database.executeUpdateQuery(sql)

        return


