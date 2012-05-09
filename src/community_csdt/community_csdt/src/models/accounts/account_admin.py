import json
import logging

from community_csdt.src.models import database
from community_csdt.src.models.accounts.admin import account_class, account_comment, account_password, account_profile, account_project

class AccountAdmin(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self.owner = self.__parent__.owner
        self.user_id = self.__parent__.user_id

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("AccountAdmin.__getitem__()")
        log.debug("key = %s" % key)

        if key == "classes":
            return account_class.AccountClass(self, key)
        elif key == "comments":
            return account_comment.AccountComment(self, key)
        elif key == "password":
            return account_password.AccountPassword(self, key)
        elif key == "profile":
            return account_profile.AccountProfile(self, key)
        elif key == "projects":
            return account_project.AccountProject(self, key)

        raise KeyError

    

