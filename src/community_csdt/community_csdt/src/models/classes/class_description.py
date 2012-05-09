import json
import logging

from community_csdt.src.models import database

class ClassDescription(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("ClassDescription.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Returns the username for the owner (teacher) of the specified class. Classroom has to be active and public or privately viewable.
    def getClassOwner(self, class_id):
        log = logging.getLogger('csdt')
        log.info("ClassDescription.getClassOwner()")
    
        sql = "SELECT un.username AS username FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND un.user_id = u.id AND c.id = %s AND cm.permissions = \'t\' AND c.active = 1 AND u.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return
        
        return result["username"]

    # Changes the class description on a specific classroom home page given their class_id. Returns 0 if successful.
    def changeClassDescription(self, class_id, description): 
        log = logging.getLogger('csdt')
        log.debug("ClassDescription.changeClassDescription()")
  
        # Updates the usernames table by changing the username for a given user id
        sql = "UPDATE classrooms SET description = \'%s\' WHERE id = %s;" % (str(description), str(class_id))
        result = database.executeUpdateQuery(sql)

        return

    
