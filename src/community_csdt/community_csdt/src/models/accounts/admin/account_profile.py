import json
import logging

from community_csdt.src.models import database

class AccountProfile(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self.owner = self.__parent__.owner
        self.user_id = self.__parent__.user_id

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("AccountProfile.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Changes the about me and location information of a user
    def changeUserAboutMe(self, user_id, about): 
        log = logging.getLogger('csdt')
        log.info("AccountProfile.changeUserAboutMe()")

        # Updates the usernames table by changing the username for a given user id
        sql = "UPDATE user_profile SET about = '%s' WHERE user_id = %s;" % (str(about), str(user_id))
        result = database.executeUpdateQuery(sql)

        return
