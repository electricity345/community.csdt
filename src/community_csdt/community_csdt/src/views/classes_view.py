import json
import logging
import math

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.classes import *

class ClassesView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Only users who are teachers and owners of the particular web page can access it
    def teacherOnlyAuthorization(self, session, class_owner):
        log = logging.getLogger('csdt')
        log.info("classes_view.teacherOnlyAuthorization()")

        # Verifies that only the owner of the web page can perform the following task (Authorization)
        if "user_id" not in session or "username" not in session or session["username"] != class_owner:
            log.warning("user_id is not in session or username is not in session or username is not the same as owner")
            raise HTTPNotFound()

        # Verifies whether or not the user is a teacher - only teachers can perform the following task (Authorization)
        if "teacher_classes" not in session:
            log.warning("user is not a teacher")
            raise HTTPForbidden()

        return

    # Verifies that the class_id is an actual class
    def verifyClassExistance(self, class_id):
        log = logging.getLogger('csdt')
        log.info("classes_view.verifyClassExistance()")      

        class_owner = self.context.getClassOwner(class_id)
        if class_owner is None:
            log.warning("class does not exist")
            raise HTTPNotFound()

        return class_owner

    # Resource url = "/classes?class_id=" - Shows the classroom home page for a specific classroom
    @view_config(context='community_csdt.src.models.classes.classroom.Classroom', name='', renderer='classroom.mako')
    def getClassroom(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getClassroom()")    

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

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)

        class_info = self.context.getClassDescription(class_id)
        if class_info is None:
            log.warning("class does not exist")
            raise HTTPNotFound()

        return {'about':class_info["description"], 'class_id':class_id, 'classname':class_info["classname"], 'created':class_info["time"], 'owner':class_owner, 'session':session}

    # Resource url = "/classes/projects-tables?class_id=" - Returns all of the projects uploaded by to a specific classroom
    @view_config(context='community_csdt.src.models.classes.classroom.Classroom', name='projects-tables', renderer='json', xhr=True)
    def getProjectsForClass(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getProjectsForClass()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        class_id = self.request.params["class_id"]
        class_owner = self.verifyClassExistance(class_id)

        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfProjectsForClass(class_id))
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

        proj_list = self.context.getAllProjectsForClass(class_id, sort_name, sort_order)
        proj_list = proj_list[begin_index:end_index]

        proj_hash = {}
        proj_hash['page'] = page_loc
        proj_hash['total'] = total_pages
        proj_hash['records'] = num_records
        proj_hash['results'] = proj_list

        for k, v in proj_hash.iteritems():
            log.debug("key = %s value = %s" % (k, v))
  
        json_dump = json.dumps(proj_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/classes/description/edit?class_id=" - Shows the edit classroom description page
    @view_config(context='community_csdt.src.models.classes.class_description.ClassDescription', name='edit', renderer='edit.class.description.mako')
    def getEditClassDescription(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getEditClassDescription()")   

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

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        return {'class_id':class_id, 'full_url':self.request.url, 'path_url':self.request.path_url, 'owner':class_owner, 'session':session}

    # Resource url = "/classes/description/edit-forms?class_id=" - Changes the classroom description for the classroom home page
    @view_config(context='community_csdt.src.models.classes.class_description.ClassDescription', name='edit-forms', renderer='json', xhr=True)
    def processEditClassDescription(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.processEditClassDescription()")
    
        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params or "description" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        description = self.request.params["description"]        
        class_id = self.request.params["class_id"]
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        self.context.changeClassDescription(class_id, description)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/classes/password/edit?class_id=" - Shows the edit classroom password page
    @view_config(context='community_csdt.src.models.classes.class_password.ClassPassword', name='edit', renderer='edit.class.password.mako')
    def getEditClassPassword(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getEditClassPassword()")   

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

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        return {'class_id':class_id, 'full_url':self.request.url, 'path_url':self.request.path_url, 'owner':class_owner, 'session':session}

    # Resource url = "/classes/password/edit-forms?class_id=" - Changes the password for a given class
    @view_config(context='community_csdt.src.models.classes.class_password.ClassPassword', name='edit-forms', renderer='json', xhr=True)
    def processEditClassPassword(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.processEditPassword()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params or "original_password" not in self.request.params or "password" not in self.request.params or "re_password" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        original_password = self.request.params["original_password"]
        password = self.request.params["password"]
        re_password = self.request.params["re_password"]

        result = self.context.verifyClassPassword(class_id, original_password)
        if result is None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        if password != re_password:
            json_hash = {'result': '-2'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        self.context.changeClassPassword(class_id, password)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/classes/comments/edit-flag-level?class_id=" - Shows the edit class comment flag level
    @view_config(context='community_csdt.src.models.classes.class_comment.ClassComment', name='edit-flag-level', renderer='edit.class.comment.flag.level.mako')
    def getEditFlagCommentLevel(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getEditFlagCommentLevel()")   

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

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        return {'class_id':class_id, 'full_url':self.request.url, 'path_url':self.request.path_url, 'owner':class_owner, 'session':session}

    # Resource url = "/classes/comments/flag-forms?class_id=" - Submits the admin control level for monitoring user comments for a specified class
    @view_config(context='community_csdt.src.models.classes.class_comment.ClassComment', name='flag-forms', renderer='json', xhr=True)
    def processClassFlaggedCommentLevel(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.processClassFlaggedCommentLevel()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
        
        if "class_id" not in self.request.params or "level" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        level = self.request.params["level"]

        self.context.changeClassFlagCommentLevel(session["user_id"], class_id, level)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)  

    # Resource url = "/classes/comments/flag-level?class_id=" - Gets the current flag level of the specified class
    @view_config(context='community_csdt.src.models.classes.class_comment.ClassComment', name='flag-level', renderer='json', xhr=True)
    def getClassFlaggedCommentLevel(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getClassFlaggedCommentLevel()")

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

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        level = self.context.getClassFlagCommentLevel(session["user_id"], class_id)
        log.debug("level = %s" % level)    

        json_hash = {'result': level}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)        

    # Resource url = "/classes/students-all?class_id=" - Shows a table of all the students in a particular class
    @view_config(context='community_csdt.src.models.classes.classroom.Classroom', name='students-all', renderer='class.students.mako')
    def getStudentsInClass(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getStudentsInClass()")
    
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

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)

        # Verifies whether or not the user is logged in. If they are not, it returns both the class name and a permission value of none. 
        # Otherwise, it returns with the user's permission from the database.        
        permissions = ""
        classname = ""
        if "user_id" not in session or "username" not in session:
            class_info = self.context.getClassDescription(class_id)
            if class_info is None:
                log.warning("class does not exist")
                raise HTTPNotFound() 

            classname = class_info["classname"]
            permissions = "none"
        else:
            class_info = self.context.determineClassPermissions(class_id, session["user_id"])
            if class_info is None:
                log.warning("class does not exist")
                raise HTTPNotFound() 

            classname = class_info["classname"]
            permissions = class_info["permissions"]

        log.debug("classname = %s" % classname)
        log.debug("permissions = %s" % permissions)

        return {'class_id':class_id, 'classname':classname, 'path_url':self.request.path_url, 'owner':class_owner, 'permissions':permissions, 'session':session}

    # Resource url = "/classes/students-all-tables?class_id=" - Returns all of the students in a particular class
    @view_config(context='community_csdt.src.models.classes.classroom.Classroom', name='students-all-tables', renderer='json', xhr=True)
    def getStudentsInClassTable(self):
        log = logging.getLogger('csdt')
        log.info("classes_view.getStudentsInClassTable()")

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

        class_id = self.request.params["class_id"]    
        class_owner = self.verifyClassExistance(class_id)

        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getIndividualClassSize(class_id))
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

        class_list = self.context.getAllPeopleInClass(class_id, sort_name, sort_order)
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

    # Resource url = "/classes/set-password-flag?class_id=&user_id=" - Sets the password flag for a given user, so that they can recover their password
    @view_config(context='community_csdt.src.models.classes.classroom.Classroom', name='set-password-flag', renderer='json', xhr=True)
    def setPasswordFlag(self):
        log = logging.getLogger('csdt')
        log.debug("classes_view.setPasswordFlag()")
    
        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "class_id" not in self.request.params or "user_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = self.request.params["user_id"]        
        class_id = self.request.params["class_id"]
        class_owner = self.verifyClassExistance(class_id)
        self.teacherOnlyAuthorization(session, class_owner)

        result = self.context.verifyUserId(user_id)
        if result is None:
            log.warning("user does not exist")
            raise HTTPNotFound()

        # Sets the password flag to 1
        self.context.raisePasswordFlag(user_id)
    
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)
    
        return Response(json_dump) 

    
