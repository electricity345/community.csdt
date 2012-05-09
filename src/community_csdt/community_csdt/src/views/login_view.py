import json
import logging

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.login import *

class LoginView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Resource url = "/login" - Shows the login page
    @view_config(context='community_csdt.src.models.login.login.Login', name='', renderer='login.mako')
    def getLogin(self):
        log = logging.getLogger('csdt')
        log.info("login_view.getLogin()")
    
        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'session':session}

    # Resource url = "/login/login-forms" - Verifies the creditions of a user logging in
    @view_config(context='community_csdt.src.models.login.login.Login', name='login-forms', renderer='json', xhr=True)
    def userVerification(self):
        log = logging.getLogger('csdt')
        log.info("login_view.userVerification()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session
    
        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "login_name" not in self.request.params or "password" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        login_name = self.request.params['login_name']
        password = self.request.params['password']

        # Verifies that the login name and subsequent password match
        user_id = self.context.authenticateUser(login_name, password)
        if user_id is None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)
            return Response(json_dump)
    
        # Begins to assign values into the session variable
        user_info = self.context.getUserProfileInformation(user_id)

        session['user_id'] = str(user_id)
        session['first_name'] = user_info["first_name"]
        session['last_name'] = user_info["last_name"]
        session['email'] = user_info["email"]
        session['permissions'] = user_info["permissions"]
        session['username'] = user_info["username"]

        if session["permissions"] == "p":
            # Gets a list of all classrooms that a user manages. Returns an empty list if they don't manage a class.
            sort_name = "class_id"
            sort_order = "ASC"
            class_list = self.context.getAllClassesEnrolledAsTeacher(session["user_id"], sort_name, sort_order)
            teacher_hash = {}
            for item in class_list:
                teacher_hash[str(item["cid"])] = item["classname"]

            if teacher_hash:
                session["teacher_classes"] = teacher_hash
 
        # Gets a list of all classrooms that a user is a part of. Returns an empty list if they aren't a part of a class.
        sort_name = "class_id"
        sort_order = "ASC"
        class_list = self.context.getAllClassesEnrolledAsStudent(session["user_id"], sort_name, sort_order)
        student_hash = {}
        for item in class_list:
            student_hash[str(item["cid"])] = item["classname"]

        if student_hash:
            session["student_classes"] = student_hash
    
        json_hash = {'result': '0', 'username': session['username']}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)
    
        return Response(json_dump)
       

