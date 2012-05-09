import json
import logging

from community_csdt.src.models import database
from community_csdt.src.models.register import register_account, register_class
from community_csdt.src.utils import date

class Register(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Register.__getitem__()")
        log.debug("key = %s" % key)

        if key == "accounts":
            return register_account.RegisterAccount(self, key)
        elif key == "classes":
            return register_class.RegisterClass(self, key)

        raise KeyError

    



