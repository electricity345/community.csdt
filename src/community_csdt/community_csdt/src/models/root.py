import json
import logging

from community_csdt.src.models.accounts import account
from community_csdt.src.models.classes import classroom
from community_csdt.src.models.galleries import gallery
from community_csdt.src.models.login import login
from community_csdt.src.models.logout import logout
from community_csdt.src.models.pages import page
from community_csdt.src.models.projects import project
from community_csdt.src.models.recover import recover
from community_csdt.src.models.register import register
from community_csdt.src.models.upload import upload
   
class Root(object):
    __name__ = None
    __parent__ = None

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Root.__init__()")
        log.debug("key = %s" % key)

        if key == "accounts":
            return account.Account(self, key)
        elif key == "classes":
            return classroom.Classroom(self, key)
        elif key == "galleries":
            return gallery.Gallery(self, key)
        elif key == "login":
            return login.Login(self, key)
        elif key == "logout":
            return logout.Logout(self, key)
        elif key == "pages":
            return page.Page(self, key)
        elif key == "projects":
            return project.Project(self, key)
        elif key == "recover":
            return recover.Recover(self, key)
        elif key == "register":
            return register.Register(self, key)
        elif key == "upload":
            return upload.Upload(self, key)

        return self


