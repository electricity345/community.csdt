import json
import logging

from community_csdt.src.models import database

class Logout(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Logout.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError
