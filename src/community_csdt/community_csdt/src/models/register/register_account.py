import json
import logging

from community_csdt.src.models import database
from community_csdt.src.models.register import register_public, register_student

class RegisterAccount(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("RegisterAccount.__getitem__()")
        log.debug("key = %s" % key)

        if key == "public":
            return register_public.RegisterPublic(self, key)
        elif key == "student":
            return register_student.RegisterStudent(self, key)

        raise KeyError

    # Checks if username already exists in database and is currently active.
    def doesUsernameExist(self, username):
        log = logging.getLogger('csdt')
        log.info("RegisterAccount.doesUsernameExist()")
  
        sql = "SELECT un.user_id AS user_id FROM usernames un, users u WHERE un.user_id = u.id AND un.username = \'%s\' AND u.active = 1;" % (str(username))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return
        
        return result["user_id"]


