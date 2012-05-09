import json
import logging
import math

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.pages import *

class PagesView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Resource url = "/pages/about" - Shows the about page
    @view_config(context='community_csdt.src.models.pages.page.Page', name='about', renderer='about.mako')
    def getAbout(self):
        log = logging.getLogger('csdt')
        log.info("pages_view.getAbout()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'session':session} 

    # Resource url = "/pages/admin" - Shows the admin page
    @view_config(context='community_csdt.src.models.pages.page.Page', name='admin', renderer='admin.mako')
    def getAdmin(self):
        log = logging.getLogger('csdt')
        log.info("pages_view.getAdmin()")    

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'session':session} 

    # Resource url = "/pages/contact" - Shows the contact page
    @view_config(context='community_csdt.src.models.pages.page.Page', name='contact', renderer='contact.mako')
    def getContact(self):
        log = logging.getLogger('csdt')
        log.info("pages_view.getContact()") 

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'session':session} 

    # Renders the terms.mako file - Routes to "/pages/terms" - Shows the terms of service page
    @view_config(context='community_csdt.src.models.pages.page.Page', name='terms', renderer='terms.mako')
    def getTerms(self):
        log = logging.getLogger('csdt')
        log.info("pages_view.getTerms()")    

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'session':session} 


