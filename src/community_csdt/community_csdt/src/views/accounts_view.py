import json
import logging
import math

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.accounts import *

class AccountsView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Only users who are teachers and owners of the particular web page can access it
    def teacherOnlyAuthorization(self, session):
        log = logging.getLogger('csdt')
        log.info("accounts_view.teacherOnlyAuthorization()")

        # Verifies that only the owner of the web page can perform the following task (Authorization)
        if "user_id" not in session or "username" not in session or session["username"] != self.context.owner:
            log.warning("user_id is not in session or username is not in session or username is not the same as owner")
            raise HTTPForbidden()

        # Verifies whether or not the user is a teacher - only teachers can perform the following task (Authorization)
        if "teacher_classes" not in session:
            log.warning("user is not a teacher")
            raise HTTPForbidden()

        return

    # Only users who are owners of the particular web page can access it
    def ownerOnlyAuthorization(self, session):
        log = logging.getLogger('csdt')
        log.info("accounts_view.ownerOnlyAuthorization()")

        # Verifies that only the owner of the web page can perform the following task (Authorization)
        if "user_id" not in session or "username" not in session or session["username"] != self.context.owner:
            log.warning("user_id is not in session or username is not in session or username is not the same as owner")
            raise HTTPForbidden()

        return

    # Resource url = "/accounts/{owner}" - Shows a user's profile page - Authentication is done in mako template
    @view_config(context='community_csdt.src.models.accounts.account.Account', name='', renderer='user.profile.mako')
    def getProfile(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getProfile()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        user_info = self.context.getUserProfileInformation(self.context.user_id)
        if user_info is None:
            log.warning("user does not exist")
            raise HTTPNotFound()

        return {'first_name':user_info["first_name"], 'last_name':user_info["last_name"], 'email':user_info["email"], 'about':user_info["about"], 'owner':self.context.owner, 'user_id':self.context.user_id, 'session':session}

    # Resource url = "/accounts/{owner}/projects" - Shows a table of all projects uploaded by a particular user - Authentication is done in mako template
    @view_config(context='community_csdt.src.models.accounts.account.Account', name='projects', renderer='user.projects.mako') 
    def getOwnProjects(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getOwnProjects()") 
 
        log.debug("context = %s" % self.context)   
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        user_info = self.context.getUserProfileInformation(self.context.user_id)
        if user_info is None:
            log.warning("user does not exist")
            raise HTTPNotFound()

        return {'first_name':user_info["first_name"], 'last_name':user_info["last_name"], 'email':user_info["email"], 'owner':self.context.owner, 'user_id':self.context.user_id, 'session':session}

    # Resource url = "/accounts/{owner}/projects-tables" - Returns all projects uploaded by a particular user - Authentication is done in mako template
    @view_config(context='community_csdt.src.models.accounts.account.Account', name='projects-tables', renderer='json', xhr=True)
    def getOwnProjectsTable(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getOwnProjectsTable()")
    
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
        num_records = int(self.context.getSizeOfActiveProjectTableForAUser(self.context.user_id))
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

        proj_list = self.context.getActiveProjectTableForAUser(self.context.user_id, sort_name, sort_order)
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

    # Resource url = "/accounts/{owner}/admin/projects/copy-to-class-list?proj_id=" - Shows a table of all classes that a user can copy a project to
    @view_config(context='community_csdt.src.models.accounts.admin.account_project.AccountProject', name='copy-to-class-list', renderer='copy.project.to.class.mako')
    def getCopyProjectToClass(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getCopyProjectToClass()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.ownerOnlyAuthorization(session)

        if "proj_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params["proj_id"]

        # Verifies whether or not the project is under the jurisdiction of the user to moderate
        verify = self.context.verifyProjectId(proj_id, session["user_id"])
        if verify is None:
            log.warning("project is not under the jurisdication of the user")
            raise HTTPForbidden()

        return {'full_url':self.request.url, 'path_url':self.request.path_url, 'owner':self.context.owner, 'proj_id':proj_id, 'session':session}

    # Resource url = "/accounts/{owner}/admin/projects/copy-to-class-list-tables?proj_id=" - Returns all classes that a user can copy a project to
    @view_config(context='community_csdt.src.models.accounts.admin.account_project.AccountProject', name='copy-to-class-list-tables', renderer='json', xhr=True)
    def getCopyProjectToClassTable(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getCopyProjectToClassTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.ownerOnlyAuthorization(session)

        if "proj_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params["proj_id"]

        # Verifies whether or not the project is under the jurisdiction of the user to moderate
        verify = self.context.verifyProjectId(proj_id, session["user_id"])
        if verify is None:
            log.warning("project is not under the jurisdication of the user")
            raise HTTPForbidden()
        
        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session['user_id']

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfEnrolledClasses(user_id))
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

        class_list = self.context.getAllEnrolledClassesWithUploadedProject(user_id, proj_id, sort_name, sort_order)
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

    # Resource url = "/accounts/{owner}/admin/projects/copy-to-class?proj_id=&class_id=" - Copies project to a class
    @view_config(context='community_csdt.src.models.accounts.admin.account_project.AccountProject', name='copy-to-class', renderer='json', xhr=True)
    def processCopyProjectToClass(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.processCopyProjectToClass()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.ownerOnlyAuthorization(session)

        if "proj_id" not in self.request.params or "class_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params["proj_id"]
        class_id = self.request.params["class_id"]

        # Verifies whether or not the project is under the jurisdiction of the user to moderate
        verify = self.context.verifyProjectId(proj_id, session["user_id"])
        if verify is None:
            log.warning("project is not under the jurisdication of the user")
            raise HTTPForbidden()

        # Verifies whether or not the user is a participant in the class
        verify = self.context.verifyUserAsClassParticipant(class_id, session["user_id"])
        if verify is None:
            log.warning("user is not a participant in the class")
            raise HTTPNotFound()
        
        self.context.copyProjectToClass(proj_id, class_id)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)  

    # Resource url = "/accounts/{owner}/admin/projects/remove-from-class?proj_id=&class_id=" - Removes project from a class
    @view_config(context='community_csdt.src.models.accounts.admin.account_project.AccountProject', name='remove-from-class', renderer='json', xhr=True)
    def processRemoveProjectFromClass(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.processRemoveProjectFromClass()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.ownerOnlyAuthorization(session)

        if "proj_id" not in self.request.params or "class_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params["proj_id"]
        class_id = self.request.params["class_id"]

        # Verifies whether or not the project is under the jurisdiction of the user to moderate
        verify = self.context.verifyProjectId(proj_id, session["user_id"])
        if verify is None:
            log.warning("project is not under the jurisdication of the user")
            raise HTTPForbidden()

        # Verifies whether or not the user is a participant in the class
        verify = self.context.verifyUserAsClassParticipant(class_id, session["user_id"])
        if verify is None:
            log.warning("user is not a participant in the class")
            raise HTTPNotFound()
        
        self.context.removeProjectFromClass(proj_id, class_id)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)  

    # Resource url = "/accounts/{owner}/admin/classes/teacher-all" - Shows a table of all classes that a particular user (teacher) manages
    @view_config(context='community_csdt.src.models.accounts.admin.account_class.AccountClass', name='teacher-all', renderer='teacher.classes.mako') 
    def getManageClasses(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getManageClasses()")    
        
        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.teacherOnlyAuthorization(session)

        return {'path_url':self.request.path_url, 'owner':self.context.owner, 'session':session}

    # Resource url = "/accounts/{owner}/admin/classes/teacher-all-tables" - Returns all of the classes that a particular user (teacher) manages
    @view_config(context='community_csdt.src.models.accounts.admin.account_class.AccountClass', name='teacher-all-tables', renderer='json', xhr=True)
    def getManageClassesTable(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getManageClassesTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.teacherOnlyAuthorization(session)

        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session['user_id']

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfClassesEnrolledAsTeacher(user_id))
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

        class_list = self.context.getAllClassesEnrolledAsTeacher(user_id, sort_name, sort_order)
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

    # Resource url = "/accounts/{owner}/admin/classes/student-all" - Shows a table of all class's that a user has joined
    @view_config(context='community_csdt.src.models.accounts.admin.account_class.AccountClass', name='student-all', renderer='student.classes.mako')
    def getOwnRegisteredClasses(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getOwnRegisteredClasses()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
 
        self.ownerOnlyAuthorization(session)

        return {'path_url':self.request.path_url, 'owner':self.context.owner, 'session':session}

    # Resource url = "/accounts/{owner}/admin/classes/student-all-tables" - Returns all classes that a user is enrolled in
    @view_config(context='community_csdt.src.models.accounts.admin.account_class.AccountClass', name='student-all-tables', renderer='json', xhr=True)
    def getOwnRegisteredClassesTable(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getOwnRegisteredClassesTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.ownerOnlyAuthorization(session)
        
        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session['user_id']

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfClassesEnrolledAsStudent(user_id))
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

        class_list = self.context.getAllClassesEnrolledAsStudent(user_id, sort_name, sort_order)
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

    # Resource url = "/accounts/{owner}/admin/comments/flag-all" - Shows a table of all flagged comments that a particular user (teacher) manages
    @view_config(context='community_csdt.src.models.accounts.admin.account_comment.AccountComment', name='flag-all', renderer='flagged.comments.mako')
    def getFlaggedComments(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getFlaggedComments()")   

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
 
        self.teacherOnlyAuthorization(session)
        
        return {'full_url':self.request.url, 'path_url':self.request.path_url, 'owner':self.context.owner, 'session':session}

    # Resource url = "/accounts/{owner}/admin/comments/flag-all-tables" - Returns all of the flagged comments that a particular user (teacher) manages
    @view_config(context='community_csdt.src.models.accounts.admin.account_comment.AccountComment', name='flag-all-tables', renderer='json', xhr=True)
    def getFlaggedCommentsTable(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getFlaggedCommentsTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.teacherOnlyAuthorization(session)
        
        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session['user_id']

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfFlaggedComments(user_id))
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

        comment_list = self.context.getAllFlaggedCommentsForATeacher(user_id, sort_name, sort_order)
        comment_list = comment_list[begin_index:end_index]

        comment_list_hash = {}
        comment_list_hash['page'] = page_loc
        comment_list_hash['total'] = total_pages
        comment_list_hash['records'] = num_records
        comment_list_hash['results'] = comment_list

        for k, v in comment_list_hash.iteritems():
            log.debug("key = %s value = %s" % (k, v))
  
        json_dump = json.dumps(comment_list_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)
      
    # Resource url = "/accounts/{owner}/admin/comments/approve?comment_id=" - Approves comment as acceptable
    @view_config(context='community_csdt.src.models.accounts.admin.account_comment.AccountComment', name='approve', renderer='json', xhr=True)
    def processApproveComment(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.processApproveComment()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.teacherOnlyAuthorization(session)

        if "comment_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session["user_id"]
        comment_id = self.request.params["comment_id"]
    
        # Verifies whether or not the comment is under the jurisdiction of the teacher to moderate
        verify = self.context.verifyCommentId(comment_id, user_id)
        if verify is None:
            log.warning("comment is not under the jurisdication of the user")
            raise HTTPForbidden()

        self.context.approveComment(comment_id)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)  

    # Resource url = "/accounts/{owner}/admin/comments/ban?comment_id=" - Bans comment and removes it
    @view_config(context='community_csdt.src.models.accounts.admin.account_comment.AccountComment', name='ban', renderer='json', xhr=True)
    def processbanComment(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.processbanComment()")    

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.teacherOnlyAuthorization(session)

        if "comment_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session["user_id"]
        comment_id = self.request.params["comment_id"]

        # Verifies whether or not the comment is under the jurisdiction of the teacher to moderate
        verify = self.context.verifyCommentId(comment_id, user_id)
        if verify is None:
            log.warning("comment is not under the jurisdication of the user")
            raise HTTPForbidden()
            
        self.context.banComment(comment_id)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)  

    # Resource url = "/accounts/{owner}/admin/comments/users-list?comment_id=" - Shows a table of all the users who flagged a particular comment
    @view_config(context='community_csdt.src.models.accounts.admin.account_comment.AccountComment', name='users-list', renderer='flagged.comment.users.mako')
    def getFlaggedCommentUsers(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getFlaggedCommentUsers()")  

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.teacherOnlyAuthorization(session)

        if "comment_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session["user_id"]
        comment_id = self.request.params["comment_id"]
  
        # Verifies whether or not the comment is under the jurisdiction of the teacher to moderate
        verify = self.context.verifyCommentId(comment_id, user_id)
        if verify is None:
            log.warning("comment is not under the jurisdication of the user")
            raise HTTPForbidden()

        return {'path_url':self.request.path_url, 'comment_id':comment_id,'owner':self.context.owner, 'session':session}

    # Resource url = "/accounts/{owner}/admin/comments/users-list-flag-tables?comment_id=" - Returns all of the users who flagged a particular comment
    @view_config(context='community_csdt.src.models.accounts.admin.account_comment.AccountComment', name='users-list-flag-tables', renderer='json', xhr=True)
    def getFlaggedCommentUsersTable(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getFlaggedCommentUsersTable()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        self.teacherOnlyAuthorization(session)

        if "comment_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session["user_id"]
        comment_id = self.request.params["comment_id"]

        # JqGrid initialization of the table
        if "rows" not in self.request.params or "sidx" not in self.request.params or "sord" not in self.request.params or "page" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()    
    
        # Verifies whether or not the comment is under the jurisdiction of the teacher to moderate
        verify = self.context.verifyCommentId(comment_id, user_id)
        if verify is None:
            log.warning("comment is not under the jurisdication of the user")
            raise HTTPForbidden()

        rows = int(self.request.params['rows'])
        log.debug("rows = %d" % rows)
        num_records = int(self.context.getNumOfFlaggedCommentUsers(comment_id))
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

        comment_list = self.context.getFlaggedCommentUsers(comment_id, sort_name, sort_order)
        comment_list = comment_list[begin_index:end_index]

        comment_list_hash = {}
        comment_list_hash['page'] = page_loc
        comment_list_hash['total'] = total_pages
        comment_list_hash['records'] = num_records
        comment_list_hash['results'] = comment_list

        for k, v in comment_list_hash.iteritems():
            log.debug("key = %s value = %s" % (k, v))
  
        json_dump = json.dumps(comment_list_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/accounts/{owner}/admin/password/edit" - Shows the edit user password page
    @view_config(context='community_csdt.src.models.accounts.admin.account_password.AccountPassword', name='edit', renderer='edit.user.password.mako')
    def getEditPassword(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getEditPassword()")    

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
 
        self.ownerOnlyAuthorization(session)

        return {'full_url':self.request.url, 'path_url':self.request.path_url, 'owner':self.context.owner, 'session':session}

    # Resource url = "/accounts/{owner}/admin/password/edit-forms" - Changes the password for a given user.
    @view_config(context='community_csdt.src.models.accounts.admin.account_password.AccountPassword', name='edit-forms', renderer='json', xhr=True)
    def processEditPassword(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.processEditPassword()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
 
        self.ownerOnlyAuthorization(session)

        if "original_password" not in self.request.params or "password" not in self.request.params or "re_password" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        original_password = self.request.params["original_password"]
        password = self.request.params["password"]
        re_password = self.request.params["re_password"]

        user_id = self.context.authenticateUser(session["username"], original_password)        
        if user_id is None:
            json_hash = {'result': '-1'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        if password != re_password:
            json_hash = {'result': '-2'}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)

            return Response(json_dump)

        self.context.changeUserPassword(session["user_id"], session["username"], password)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/accounts/{owner}/admin/profile/edit" - Shows the edit profile page
    @view_config(context='community_csdt.src.models.accounts.admin.account_profile.AccountProfile', name='edit', renderer='edit.user.profile.mako')
    def getEditProfile(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.getEditProfile()")    

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
 
        self.ownerOnlyAuthorization(session)

        return {'full_url':self.request.url, 'path_url':self.request.path_url, 'owner':self.context.owner, 'session':session}

    # Resource url = "/accounts/{owner}/admin/profile/edit-forms" - Changes the profile page of a user
    @view_config(context='community_csdt.src.models.accounts.admin.account_profile.AccountProfile', name='edit-forms', renderer='json', xhr=True)
    def processEditProfile(self):
        log = logging.getLogger('csdt')
        log.info("accounts_view.processEditProfile()")
 
        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))
 
        self.ownerOnlyAuthorization(session)

        if "about" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        user_id = session["user_id"]
        about = self.request.params["about"]

        self.context.changeUserAboutMe(user_id, about)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)    


