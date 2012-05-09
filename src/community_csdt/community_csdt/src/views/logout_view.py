import json
import logging

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.logout import logout

class LogoutView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Resource url = "/logout" - Shows the logout page
    @view_config(context='community_csdt.src.models.logout.logout.Logout', name='', renderer='logout.mako')
    def getLogout(self):
        log = logging.getLogger('csdt')
        log.info("logout_view.getLogout()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        session.delete()
        return {'session':session}
