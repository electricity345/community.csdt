import json
import logging
import math

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config
from recaptcha.client import captcha

from community_csdt.src.models.recover import *

class RecoverView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Only users who are not logged in can access the following web page
    def nonUsersOnlyAuthorization(self, session):
        log = logging.getLogger('csdt')
        log.info("recover_view.nonUsersOnlyAuthorization()")

        # Verifies that only the owner of the web page can perform the following task (Authorization)
        if "user_id" in session:
            log.warning("user is logged in")
            raise HTTPNotFound()

        return 

    # Only users who are owners of the particular web page can access it
    def ownerOnlyAuthorization(self, session):
        log = logging.getLogger('csdt')
        log.info("recover_view.ownerOnlyAuthorization()")

        # Verifies that only the owner of the web page can perform the following task (Authorization)
        if "user_id" not in session or "username" not in session:
            log.warning("user_id is not in session or username is not in session")
            raise HTTPNotFound()

        return

    # Resource url = "/recover/password" - Shows the recover password page
    @view_config(context='community_csdt.src.models.recover.recover.Recover', name='password', renderer='recover.user.password.mako')
    def getRecoverPassword(self):
        log = logging.getLogger('csdt')
        log.info("recover_view.getRecoverPassword()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.nonUsersOnlyAuthorization(session)

        return {'path_url':self.request.path_url, 'session':session} 

    # Resource url = "/recover/password-forms" 
    # Verifies the creditions of the username or email, resets their password and sends them a new password to their email for them to reset
    @view_config(context='community_csdt.src.models.recover.recover.Recover', name='password-forms', renderer='json', xhr=True)
    def processRecoverPassword(self):
        log = logging.getLogger('csdt')
        log.info("recover_view.processRecoverPassword()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "input_string" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()
    
        self.nonUsersOnlyAuthorization(session)

        host = self.request.host
        recaptcha_private_key = '6Ldi2MYSAAAAALJ_KaLfTzOTAg5iNHqOmvmgaQOg'
        captcha_result = captcha.submit(
            self.request.params['recaptcha_challenge_field'],
            self.request.params['recaptcha_response_field'],
            recaptcha_private_key,
            host,
        )
        if not captcha_result.is_valid:
            error = captcha_result.error_code
            json_hash = {'result': '-1', 'error':error}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        input_string = self.request.params['input_string']
        user_id = self.context.doesUsernameExist(input_string)

        if user_id is not None:
            log.debug("username exists")
            user_info = self.context.getUserProfileInformation(user_id)
            username = user_info["username"]
            email = user_info["email"]
            permissions = user_info["permissions"]
            reset_pass = user_info["reset_pass"]
            reset_pass_counter = user_info["reset_pass_counter"]

            if email is None and permissions == 's' and reset_pass == 1: # checks if student is eligible to change their password
                log.debug("email is none, permissions is student, and reset password is 1")
                pass_counter = self.context.updateResetPasswordCounter(user_id, reset_pass_counter) 
                plaintext = username + ";" + str(pass_counter)
                ciphertext = self.context.encryptUrlQuery(unicode(plaintext))
                recover_pass_url = self.context.createAccountRecoveryUrl(self.request.host_url, ciphertext)
                    
                json_hash = {'result': '1', 'url':recover_pass_url}
                json_dump = json.dumps(json_hash)
                log.debug("json dump = %s" % json_dump)           
 
                return Response(json_dump)
            elif email is not None: 
                pass_counter = self.context.updateResetPasswordCounter(user_id, reset_pass_counter) 
                plaintext = username + ";" + str(pass_counter)
                ciphertext = self.context.encryptUrlQuery(unicode(plaintext))
                self.context.createAccountRecoveryLetter(self.request.host_url, username, email, ciphertext)

                json_hash = {'result': '0'}
                json_dump = json.dumps(json_hash)
                log.debug("json dump = %s" % json_dump)

                return Response(json_dump)
            else:
                log.debug("email is not none, permissions is not student, or reset password is 0")
                json_hash = {'result': '-2'}
                json_dump = json.dumps(json_hash)
                log.debug("json dump = %s" % json_dump)

                return Response(json_dump)

        user_id = self.context.doesEmailExist(input_string)
        if user_id is not None:
            log.debug("email exists")
            user_info = self.context.getUserProfileInformation(user_id)
            username = user_info["username"]
            email = user_info["email"]
            reset_pass_counter = user_info["reset_pass_counter"]

            pass_counter = self.context.updateResetPasswordCounter(user_id, reset_pass_counter) 
            plaintext = username + ";" + str(pass_counter)
            ciphertext = self.context.encryptUrlQuery(unicode(plaintext))
            self.context.createAccountRecoveryLetter(self.request.host_url, username, email, ciphertext)

            json_hash = {'result': '0'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        json_hash = {'result': '-3'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)    

    # Resource url = "/recover/account" - Shows the edit password page (Called from the email sent by recover_view.processRecoverPassword())
    @view_config(context='community_csdt.src.models.recover.recover.Recover', name='account', renderer='recover.user.account.mako')
    def getRecoverAccount(self):
        log = logging.getLogger('csdt')
        log.info("recover_view.getRecoverAccount()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "value" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        self.nonUsersOnlyAuthorization(session)
    
        ciphertext = self.request.params["value"]
        log.debug("ciphertext = %s" % ciphertext)
        plaintext = self.context.decryptUrlQuery(ciphertext)
        log.debug("plaintext = %s" % plaintext)

        if plaintext == "":
            log.warning("decryption function has raised an exception")
            msg = "There seems to be an error with the registration link. This can be due to your url being tampered with or because the link has expired. If the problem persists, please re-register for a new account."
            raise HTTPNotFound(body_template=msg)

        plain_list = plaintext.split(";")
        if len(plain_list) != 3:
            log.warning("plaintext has been tampered with")
            msg = "There seems to be an error with the registration link. It seems that the link has been tampered with."
            raise HTTPNotFound(body_template=msg)

        username = plain_list[1]
        user_id = self.context.doesUsernameExist(username)
        if user_id is None:
            log.warning("username has been tampered with")
            msg = "There seems to be an error with the registration link. It seems that the link has been tampered with."
            raise HTTPNotFound(body_template=msg)

        # Checks the password counter in order to prevent replay attacks
        pass_counter = plain_list[2]
        user_info = self.context.getUserProfileInformation(user_id)
        reset_pass_counter = user_info["reset_pass_counter"]
        log.debug("pass_counter = %s" % pass_counter)
        log.debug("reset_pass_counter = %s" % reset_pass_counter)
        if int(pass_counter) != int(reset_pass_counter):
            log.warning("pass_counter != reset_pass_counter")
            msg = "This link has expired."
            raise HTTPNotFound(body_template=msg)

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
    
        return {'path_url':self.request.path_url, 'username':username, 'session':session}

    # Resource url = "/recover/account-forms" - Changes the password for a given user.
    @view_config(context='community_csdt.src.models.recover.recover.Recover', name='account-forms', renderer='json', xhr=True)
    def processRecoverAccount(self):
        log = logging.getLogger('csdt')
        log.info("recover_view.processRecoverAccount()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "password" not in self.request.params or "re_password" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        self.ownerOnlyAuthorization(session)

        user_id = session["user_id"]
        password = self.request.params["password"]
        re_password = self.request.params["re_password"]
    
        if password != re_password:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        self.context.changeUserPassword(user_id, password)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)    


