import json
import logging

from community_csdt.src.models import database

class ClassComment(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("ClassComment.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Returns the username for the owner (teacher) of the specified class. Classroom has to be active and public or privately viewable.
    def getClassOwner(self, class_id):
        log = logging.getLogger('csdt')
        log.info("ClassComment.getClassOwner()")
    
        sql = "SELECT un.username AS username FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND un.user_id = u.id AND c.id = %s AND cm.permissions = 't' AND c.active = 1 AND u.active = 1;" % (str(class_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("class does not exist")
            return
        
        return result["username"]

    # Changes the admin control level for monitoring user comments. A level 0 indicates partial, while a level 1 indicates full control.
    def changeClassFlagCommentLevel(self, user_id, class_id, level):
        log = logging.getLogger('csdt')
        log.info("ClassComment.changeClassFlagCommentLevel()")
      
        # Updates the classrooms table by changing the flag comments level for all classrooms owned by a particular owner
        sql = "UPDATE classrooms SET flag_comment_level = %s WHERE id = %s AND owner = %s;" % (str(level), str(class_id), str(user_id))
        result = database.executeUpdateQuery(sql)

        return

    # Gets the current admin control level for monitoring user comments
    def getClassFlagCommentLevel(self, user_id, class_id):
        log = logging.getLogger('csdt')
        log.info("ClassComment.getClassFlagCommentLevel()")

        sql = "SELECT flag_comment_level FROM classrooms WHERE id = %s AND owner = %s;" % (str(class_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")

        return result["flag_comment_level"]


