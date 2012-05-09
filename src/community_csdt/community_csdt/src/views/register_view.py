import json
import logging
import math

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config
from recaptcha.client import captcha

from community_csdt.src.models.register import *

class RegisterView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Only users who are not logged in can access the following web page
    def nonUsersOnlyAuthorization(self, session):
        log = logging.getLogger('csdt')
        log.info("register_view.nonUsersOnlyAuthorization()")

        # Verifies that only the owner of the web page can perform the following task (Authorization)
        if "user_id" in session:
            log.warning("user is logged in")
            raise HTTPForbidden()

        return 

    # Only users who are owners of the particular web page can access it
    def ownerOnlyAuthorization(self, session, user_id):
        log = logging.getLogger('csdt')
        log.info("register_view.ownerOnlyAuthorization()")

        # Verifies that only the owner of the web page can perform the following task (Authorization)
        if "user_id" not in session or "username" not in session or session["user_id"] != user_id:
            log.warning("user_id is not in session or username is not in session or user_id is not the same as user_id in session")
            raise HTTPForbidden()

        return

    # Only public users can access the particular web page
    def publicUserOnlyAuthorization(self, session):
        log = logging.getLogger('csdt')
        log.info("register_view.publicUserOnlyAuthorization()")

        # Verifies that only public users can access page
        if "user_id" not in session or "username" not in session or "permissions" not in session or session["permissions"] == "s":
            log.warning("user_id is not in session or user is a student")
            raise HTTPForbidden()

        return 

    # Verifies that the class_id is an actual class
    def verifyClassExistance(self, class_id):
        log = logging.getLogger('csdt')
        log.info("register_view.verifyClassExistance()")      

        class_owner = self.context.getClassOwner(class_id)
        if class_owner is None:
            log.warning("class does not exist")
            raise HTTPNotFound()

        return class_owner

    # Resource url = "/register" - Shows the register page, where the user can register as a public or as a student user
    @view_config(context='community_csdt.src.models.register.register.Register', name='', renderer='register.options.mako')
    def getRegister(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getRegister()")    

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

        return {'session':session}

    # Resource url = "/register/accounts/public" - Shows the first part of the public registration portion
    @view_config(context='community_csdt.src.models.register.register_public.RegisterPublic', name='', renderer='public.registration.part.1.mako')
    def getPublicRegistration(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getPublicRegistration()")
 
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

        return {'session':session}
    
    # Resource url = "/register/accounts/public/forms" - Verifies that initial user registration conforms to standards. Sends user an email if success.
    @view_config(context='community_csdt.src.models.register.register_public.RegisterPublic', name='forms', renderer='json', xhr=True)
    def processPublicRegistration(self):
        log = logging.getLogger('csdt')
        log.debug("register_view.processPublicRegistration()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
        
        if "first_name" not in self.request.params or "last_name" not in self.request.params or "email" not in self.request.params:
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

        first_name = self.request.params['first_name']
        last_name = self.request.params['last_name']
        email = self.request.params['email']
   
        user_id = self.context.doesEmailExist(email)
        if user_id is not None:
            json_hash = {'result': '-2'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        plaintext = first_name + ";" + last_name + ";" + email
        ciphertext = self.context.encryptUrlQuery(unicode(plaintext))

        self.context.createConfirmationLetter(self.request.host_url, email, first_name, last_name, ciphertext)

        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/register/accounts/public/new" - Shows the public registration page
    @view_config(context='community_csdt.src.models.register.register_public.RegisterPublic', name='new', renderer='public.registration.part.2.mako')
    def getRegisterPublicUser(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getRegisterPublicUser()")

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
        if len(plain_list) != 4:
            log.warning("plaintext has been tampered with")
            msg = "There seems to be an error with the registration link. It seems that the link has been tampered with."
            raise HTTPNotFound(body_template=msg)

        first_name = plain_list[1]
        last_name = plain_list[2]
        email = plain_list[3]

        user_id = self.context.doesEmailExist(email)
        if user_id is not None:
            log.warning("email already exists")
            msg = "The registration link has expired. Please re-register for a new account."
            raise HTTPNotFound(body_template=msg)

        return {'full_url':self.request.url, 'email':email, 'first_name':first_name, 'last_name':last_name, 'session':session}

    # Resource url = "/register/accounts/public/new-forms" - Attempts to create a new user account.
    @view_config(context='community_csdt.src.models.register.register_public.RegisterPublic', name='new-forms', renderer='json', xhr=True)
    def processRegisterPublicUser(self):
        log = logging.getLogger('csdt')
        log.info("register_view.processRegisterPublicUser()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "first_name" not in self.request.params or "last_name" not in self.request.params or "username" not in self.request.params or "password" not in self.request.params or "re_password" not in self.request.params or "email" not in self.request.params:
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

        first_name = self.request.params['first_name']
        last_name = self.request.params['last_name']
        username = self.request.params['username']
        password = self.request.params['password']
        re_password = self.request.params['re_password']
        email = self.request.params['email']

        if password != re_password:
            json_hash = {'result': '-2'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)
     
        user_id = self.context.doesUsernameExist(username)
        if user_id is not None:
            json_hash = {'result': '-3'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        user_id = self.context.doesEmailExist(email)
        if user_id is not None:
            json_hash = {'result': '-4'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        user_id = self.context.createPublicAccount(first_name, last_name, username, password, email)
        if user_id is None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)
    
        user_info = self.context.getUserProfileInformation(user_id)
        session['user_id'] = str(user_id)
        session['first_name'] = user_info["first_name"]
        session['last_name'] = user_info["last_name"]
        session['email'] = user_info["email"]
        session['permissions'] = user_info["permissions"]
        session['username'] = user_info["username"]

        json_hash = {'result': '0', 'username': username}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)
  
        return Response(json_dump)

    # Resource url = "/register/accounts/check-username?username=" - Checks if username exists in database
    @view_config(context='community_csdt.src.models.register.register_account.RegisterAccount', name='check-username', renderer='json', xhr=True)
    def checkUsername(self):
        log = logging.getLogger('csdt')
        log.info("register_view.checkUsername()")
 
        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
        
        if "username" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        self.nonUsersOnlyAuthorization(session)

        username = self.request.params['username']

        user_id = self.context.doesUsernameExist(username)
        if user_id is not None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/register/classes/all" - Shows a table of all visible and active classes for registration
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='all', renderer='registable.classes.mako')
    def getAllRegistableClasses(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getAllRegistableClasses()")    

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
    
    # Resource url = "/register/classes/all-tables" - Returns all visible and active classes for registration
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='all-tables', renderer='json', xhr=True)
    def getAllRegistableClassesTable(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getAllRegistableClassesTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfRegistableClasses())
        log.debug("num_records = %d" % num_records)

        total_pages = int(math.ceil((num_records / float(rows))))
        log.debug("total - number of pages = %d" % total_pages)

        sort_name = self.request.params['sidx']
        sort_order = self.request.params['sord']
    
        page_loc = int(self.request.params['page'])
        begin_index = (page_loc - 1) * rows
        end_index = begin_index + rows
        log.debug("begin index value = %d" % begin_index)
        log.debug("end index value = %d" % end_index)
    
        if end_index > num_records:
            end_index = num_records

        class_list = self.context.getAllRegistableClasses(sort_name, sort_order)
        class_list = class_list[begin_index:end_index]

        class_list_hash = {}
        class_list_hash['page'] = page_loc
        class_list_hash['total'] = total_pages
        class_list_hash['records'] = num_records
        class_list_hash['results'] = class_list

        for k, v in class_list_hash.iteritems():
            log.debug("key = %s value = %s" % (k, v))
  
        json_dump = json.dumps(class_list_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/register/classes/all-registerable-tables?user_id=" - Returns all visible and active classes for registration by a user
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='all-registerable-tables', renderer='json', xhr=True)
    def getOwnRegistableClassesTable(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getOwnRegistableClassesTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "user_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = self.request.params['user_id']
        self.ownerOnlyAuthorization(session, user_id)
      
        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfRegistableClasses())
        log.debug("num_records = %d" % num_records)

        total_pages = int(math.ceil((num_records / float(rows))))
        log.debug("total - number of pages = %d" % total_pages)

        sort_name = self.request.params['sidx']
        sort_order = self.request.params['sord']
    
        page_loc = int(self.request.params['page'])
        begin_index = (page_loc - 1) * rows
        end_index = begin_index + rows
        log.debug("begin index value = %d" % begin_index)
        log.debug("end index value = %d" % end_index)
    
        if end_index > num_records:
            end_index = num_records

        class_list = self.context.getAllRegistableClassesForAUser(user_id, sort_name, sort_order)
        class_list = class_list[begin_index:end_index]

        class_list_hash = {}
        class_list_hash['page'] = page_loc
        class_list_hash['total'] = total_pages
        class_list_hash['records'] = num_records
        class_list_hash['results'] = class_list

        for k, v in class_list_hash.iteritems():
            log.debug("key = %s value = %s" % (k, v))
  
        json_dump = json.dumps(class_list_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/register/classes/sign-up?class_id=" - Shows the sign-up page to register for a particular class
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='sign-up', renderer='class.signup.mako')
    def getRegisterClassSigup(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getRegisterClassSigup()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        class_id = self.request.params['class_id']
        class_owner = self.verifyClassExistance(class_id)

        # Check if user has already registered for the particular class
        if "user_id" in session and "username" in session:
            result = self.context.isUserApartOfClass(session["user_id"], class_id)
            if result is not None:
                log.warning("user is not apart of the particular class")
                raise HTTPNotFound()

        class_info = self.context.getClassDescription(class_id)
        if class_info is None:
            log.warning("class does not exist")
            raise HTTPNotFound()

        return {'class_id':class_id, 'classname':class_info["classname"], 'full_url':self.request.url, 'owner':class_owner, 'path_url':self.request.path_url, 'session':session}

    # Resource url = "/register/classes/sign-up-forms?class_id=" - Checks if the password submitted by the user matches that of the class's
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='sign-up-forms', renderer='json', xhr=True)
    def processRegisterClassSignup(self):
        log = logging.getLogger('csdt')
        log.info("register_view.processRegisterClassSignup()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params or "password" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        class_id = self.request.params['class_id']
        class_owner = self.verifyClassExistance(class_id)

        # Check if user has already registered for the particular class
        if "user_id" in session and "username" in session:
            result = self.context.isUserApartOfClass(session["user_id"], class_id)
            if result is not None:
                log.warning("user is not apart of the particular class")
                raise HTTPNotFound()

        # Verifies that the given password matches the classroom's password
        password = self.request.params["password"]
        result = self.context.verifyClassPassword(class_id, password)
        if result is None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        # Registers the user into the new class and adds the newly registered class_id into the session variable
        if "user_id" in session and "username" in session:
            self.context.registerClass(session["user_id"], class_id)
            class_info = self.context.getClassDescription(class_id)
            if class_info is None:
                log.warning("class does not exist")
                raise HTTPNotFound()
          
            if "student_classes" in session:
                student_hash = session["student_classes"]
                student_hash[class_id] = class_info["classname"]
                session["student_classes"] = student_hash
            else:
                student_hash = {}
                student_hash[class_id] = class_info["classname"]
                session["student_classes"] = student_hash

            log.debug("session student_classes = %s" % session["student_classes"])
        else:
            # Verifies that unregistered user has passed the classroom password check
            session["registered_class_id"] = str(class_id) 
            log.debug("session[%s] = %s" % ("registered_class_id", session["registered_class_id"]))

        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/register/accounts/student/new?class_id=" - Shows the student registration page
    @view_config(context='community_csdt.src.models.register.register_student.RegisterStudent', name='new', renderer='student.registration.mako')
    def getStudentRegistration(self):
        log = logging.getLogger('csdt')
        log.info("register_view.getStudentRegistration()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        self.nonUsersOnlyAuthorization(session)

        class_id = self.request.params['class_id']
        class_owner = self.verifyClassExistance(class_id)

        # Verifies that unregistered user has passed the classroom password check
        if "registered_class_id" not in session or int(class_id) != int(session["registered_class_id"]):
            log.warning("user has not passed classroom password verification")
            raise HTTPNotFound()

        class_info = self.context.getClassDescription(class_id)
        if class_info is None:
            log.warning("class does not exist")
            raise HTTPNotFound()

        return {'class_id':class_id, 'classname':class_info["classname"], 'full_url':self.request.url, 'owner':class_owner, 'path_url':self.request.path_url, 'session':session}

    # Resource url = "/register/accounts/student/new-forms?class_id=" - Attempts to create a new user student account. Returns 0 if success. 
    @view_config(context='community_csdt.src.models.register.register_student.RegisterStudent', name='new-forms', renderer='json', xhr=True)
    def processStudentRegistration(self):
        log = logging.getLogger('csdt')
        log.info("register_view.processStudentRegistration()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params or "first_name" not in self.request.params or "last_name" not in self.request.params or "username" not in self.request.params or "password" not in self.request.params or "re_password" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()    

        self.nonUsersOnlyAuthorization(session)
        
        class_id = self.request.params['class_id']
        class_owner = self.verifyClassExistance(class_id)

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

        first_name = self.request.params['first_name']
        last_name = self.request.params['last_name']
        username = self.request.params['username']
        password = self.request.params['password']
        re_password = self.request.params['re_password']

        if password != re_password:
            json_hash = {'result': '-2'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)
       
            return Response(json_dump)

        user_id = self.context.doesUsernameExist(username)
        if user_id is not None:
            json_hash = {'result': '-3'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        user_id = self.context.createStudentAccount(first_name, last_name, username, password, class_id)
        if user_id is None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)
    
        user_info = self.context.getUserProfileInformation(user_id)
        session['user_id'] = str(user_id)
        session['first_name'] = user_info["first_name"]
        session['last_name'] = user_info["last_name"]
        session['email'] = user_info["email"]
        session['permissions'] = user_info["permissions"]
        session['username'] = user_info["username"]

        class_info = self.context.getClassDescription(class_id)
        if class_info is None:
            log.warning("class does not exist")
            raise HTTPNotFound()

        student_hash = {}
        student_hash[class_id] = class_info["classname"]
        session["student_classes"] = student_hash

        json_hash = {'result': '0', 'username': username}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/register/classes/new" - Shows a registration form for the creation of a new class
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='new', renderer='create.class.mako')
    def createClass(self):
        log = logging.getLogger('csdt')
        log.info("register_view.createClass()") 

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
  
        self.publicUserOnlyAuthorization(session)

        return {'full_url':self.request.url, 'session':session}

    # Resource url = "/register/classes/check-classname" - Checks if classname exists in database
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='check-classname', renderer='json', xhr=True)
    def checkClassname(self):
        log = logging.getLogger('csdt')
        log.info("register_view.checkClassname()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "classname" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        self.publicUserOnlyAuthorization(session)

        classname = self.request.params['classname']
        
        result = self.context.doesClassnameExist(classname)
        if result is not None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)
       
            return Response(json_dump)

        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/register/classes/new-forms" - Attempts to create a new class. Returns 0 if success. 
    @view_config(context='community_csdt.src.models.register.register_class.RegisterClass', name='new-forms', renderer='json', xhr=True)
    def processCreateClassroom(self):
        log = logging.getLogger('csdt')
        log.info("register_view.processCreateClassroom()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "classname" not in self.request.params or "comment_flag_level" not in self.request.params or "password" not in self.request.params or "re_password" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        self.publicUserOnlyAuthorization(session)
    
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

        classname = self.request.params['classname']
        level = self.request.params['comment_flag_level']
        password = self.request.params['password']
        re_password = self.request.params['re_password']

        if password != re_password:
            json_hash = {'result': '-2'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)
       
            return Response(json_dump)

        result = self.context.doesClassnameExist(classname)
        if result is not None:
            json_hash = {'result': '-3'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        class_id = self.context.createClass(session["user_id"], classname, password, level)
        if "teacher_classes" in session:
            teacher_hash = session["teacher_classes"]
            teacher_hash[class_id] = classname
            session["teacher_classes"] = teacher_hash
        else:
            teacher_hash = {}
            teacher_hash[class_id] = classname
            session["teacher_classes"] = teacher_hash

        log.debug("session teacher_classes = %s" % session["teacher_classes"])

        json_hash = {'result': '0', 'owner':session['username']}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)
    
        return Response(json_dump)    


