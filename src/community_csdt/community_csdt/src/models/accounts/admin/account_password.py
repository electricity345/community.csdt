import json
import logging

from community_csdt.src.models import database

class AccountPassword(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self.owner = self.__parent__.owner
        self.user_id = self.__parent__.user_id

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("AccountPassword.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Checks user credentials. Returns user id if user authentication is successful.
    def authenticateUser(self, username, password):
        log = logging.getLogger('csdt')
        log.info("AccountPassword.authenticateUser()")

        sql = "SELECT un.user_id AS user_id FROM usernames un, users u WHERE un.user_id = u.id AND un.username = '%s' AND un.pass = '%s' AND u.active = 1;" % (str(username), str(password))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return

        return result["user_id"]

    # Changes the password of a user
    def changeUserPassword(self, user_id, username, password): 
        log = logging.getLogger('csdt')
        log.info("AccountPassword.changeUserPassword()")
 
        # Changes the password for the user
        sql = "UPDATE usernames SET pass = '%s' WHERE user_id = %s;" % (str(password), str(user_id))
        result = database.executeUpdateQuery(sql)

        # Resets password flag to 0 for the user
        sql = "UPDATE users SET reset_pass = 0 WHERE id = %s;" % (str(user_id))
        result = database.executeUpdateQuery(sql)

        return


