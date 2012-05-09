import logging

from pyramid.response import Response
from pyramid.view import view_config

class HomeView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Resource url = "/" - Shows the home page
    @view_config(context='community_csdt.src.models.root.Root', name='', renderer='index.mako')
    def getHome(self):
        log = logging.getLogger('csdt')
        log.info("home_view.getHome()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)    
        session = self.request.session

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'session':session}




