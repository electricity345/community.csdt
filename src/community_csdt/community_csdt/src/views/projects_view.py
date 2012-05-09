import json
import logging
import math

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from community_csdt.src.models.projects import *

class ProjectsView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    # Resource url = "/projects/all" - Shows a table of all visible and active projects
    @view_config(context='community_csdt.src.models.projects.project.Project', name='all', renderer='all.projects.mako')
    def getAllProjects(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.getAllProjects()")
 
        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)
        log.debug("request view_name = %s" % self.request.view_name)
        log.debug("request path_info = %s" % self.request.path_info)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        return {'session':session}

    # Resource url = "/projects/tables" - Returns all of the projects that are both active and visible
    @view_config(context='community_csdt.src.models.projects.project.Project', name='all-tables', renderer='json', xhr=True)
    def getAllProjectsTable(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.getAllProjectsTable()")
    
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
        num_records = int(self.context.getSizeOfActiveProjectTable())
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

        proj_list = self.context.getActiveProjectTable(sort_name, sort_order)
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

    # Resource url = "/projects?proj_id=" - Shows a single user's project
    @view_config(context='community_csdt.src.models.projects.project.Project', name='', renderer='project.mako')
    def getOneProject(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.getOneProject()") 

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        proj_info = {}
        if "username" in self.request.params:
            log.debug("username found in request.params")
            proj_info["proj_id"] = self.request.params["proj_id"]
            proj_info["username"] = self.request.params["username"]
            proj_info["proj_name"] = self.request.params["proj_name"]
            proj_info["proj_type"] = self.request.params["proj_type"]
            proj_info["description"] = self.request.params["description"]
            proj_info["num_views"] = self.request.params["num_views"]
            proj_info["ratings"] = self.request.params["ratings"]
            proj_info["downloads"] = self.request.params["downloads"]        
            proj_info["stored_proj_name"] = self.request.params["stored_proj_name"]
            proj_info["time"] = self.request.params["time"]   
        else:
            proj_info = self.context.getSingleProject(proj_id)
            if proj_info is None:
               log.warning("project does not exist")
               raise HTTPNotFound()

        owner = self.context.getProjectOwner(proj_id)
        self.context.incrementViewCount(proj_id)
        proj_info["num_views"] = int(proj_info["num_views"]) + 1

        stored_proj_name = proj_info["stored_proj_name"].replace(" ", "%20")
        log.debug("stored_proj_name = %s" % stored_proj_name)

        jnlp_filename = stored_proj_name + ".jnlp"
        jnlp_path = self.request.host_url + "/uploads/projects/" + proj_type.upper() + "/jnlp/" + jnlp_filename

        return {'jnlp_path':jnlp_path, 'full_url':self.request.url, 'path_url':self.request.path_url, 'proj_id':proj_info["proj_id"], 'username':proj_info["username"], 'proj_name':proj_info["proj_name"], 'proj_type':proj_info["proj_type"], 'description':proj_info["description"], 'num_views':proj_info["num_views"], 'ratings':proj_info["ratings"], 'downloads':proj_info["downloads"], 'time':proj_info["time"], 'owner':owner, 'session':session}

    # Resource url = "/projects/average-ratings?proj_id=" - Returns the average rating for a given project
    @view_config(context='community_csdt.src.models.projects.project.Project', name='average-ratings', renderer='json', xhr=True)
    def getProjectRatings(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.getProjectRatings()") 

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
 
        if "proj_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        result = self.context.getAvgProjRating(proj_id)
        json_hash = {'avg_rating': float(result["average_ratings"]), 'num_reviews': result["num_reviews"]}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/projects/submit-rating?proj_id=" - Adds a given user's rating to a given project
    @view_config(context='community_csdt.src.models.projects.project.Project', name='submit-rating', renderer='json', xhr=True)
    def addProjectRating(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.addProjectRating()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params or "rating" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']
        rating = self.request.params['rating']

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        if "user_id" not in session:
            log.warning("user_id not found in session")
            raise HTTPBadRequest()

        user_id = session["user_id"]

        self.context.addProjectRating(proj_id, user_id, rating)
        json_hash = {'result': rating}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/projects/user-rating?proj_id=" - Returns a given user's rating for a given project
    @view_config(context='community_csdt.src.models.projects.project.Project', name='user-rating', renderer='json', xhr=True)
    def getProjectUserRating(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.getProjectUserRating()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        if "user_id" not in session:
            log.warning("user_id not found in session")
            raise HTTPBadRequest()

        user_id = session["user_id"]

        rating = self.context.getProjRatingForAUser(proj_id, user_id)
        if rating is None:
            log.warning("user has not submitted a rating for the particular project")
            rating = 0

        json_hash = {'rating': rating}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/projects/comments/add?proj_id=" - Adds a new comment to a specific project
    @view_config(context='community_csdt.src.models.projects.project_comment.ProjectComment', name='add', renderer='json', xhr=True)
    def addProjectComment(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.addProjectComment()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params or "body" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']
        body = self.request.params["body"]

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        if "user_id" not in session:
            log.warning("user_id not found in session")
            raise HTTPBadRequest()

        self.context.addProjectComment(proj_id, session["user_id"], body)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)
       
        return Response(json_dump)

    # Resource url = "/projects/comments/all?proj_id=" - Changes the profile page of a user
    @view_config(context='community_csdt.src.models.projects.project_comment.ProjectComment', name='all', renderer='json', xhr=True)
    def getAllProjectComments(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.getAllProjectComments()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        comment_list = self.context.getCommentsForAProject(proj_id)
        if comment_list is None:
            log.warning("comments do not exist for project")
            raise HTTPNotFound()
 
        json_hash = {'result':comment_list, 'dict_length':len(comment_list)}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Renders a JSON request - Routes to "/projects/comments/flag?proj_id=" - Flags a comment from a project
    @view_config(context='community_csdt.src.models.projects.project_comment.ProjectComment', name='flag', renderer='json', xhr=True)
    def flagProjectComment(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.flagProjectComment()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params or "comment_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']
        comment_id = self.request.params["comment_id"]

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        if "user_id" not in session:
            log.warning("user_id not found in session")
            json_hash = {'result': -1}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)
            return Response(json_dump)

        user_id = session["user_id"]

        self.context.setProjectCommentFlag(comment_id, user_id)
        json_hash = {'result': 1}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resource url = "/projects/comments/submit-rating?proj_id=" - Adds the ratings by a user for a specific comment in a project
    @view_config(context='community_csdt.src.models.projects.project_comment.ProjectComment', name='submit-rating', renderer='json', xhr=True)
    def submitProjectCommentRating(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.submitProjectCommentRating()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params or "rating" not in self.request.params or "comment_id" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']
        rating = self.request.params['rating']
        comment_id = self.request.params["comment_id"]

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        if "user_id" not in session:
            log.warning("user_id not found in session")
            json_hash = {'result': -1}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)
            return Response(json_dump)

        user_id = session["user_id"]

        value = self.context.addProjectCommentRating(comment_id, user_id, rating)
        if value == 1: # User has already added a rating to the specific comment
            json_hash = {'result': -2}
            json_dump = json.dumps(json_hash)
            log.debug("json dump = %s" % json_dump)
            return Response(json_dump)

        json_hash = {'result': rating}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)

    # Resoruce url = "/projects/description-edit-forms?proj_id=" - Changes the project description for a specific project
    @view_config(context='community_csdt.src.models.projects.project.Project', name='description-edit-forms', renderer='json', xhr=True)
    def processProjectDescription(self):
        log = logging.getLogger('csdt')
        log.info("projects_view.processProjectDescription()")

        log.debug("context = %s" % self.context)
        log.debug("request = %s" % self.request)   
        session = self.request.session

        log.debug("request values:")
        for k, v in self.request.params.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        log.debug("session values:")
        for k, v in session.iteritems():
            log.debug("key = %s value = %s" % (k, v))

        if "proj_id" not in self.request.params or "description" not in self.request.params:
            log.warning("request.params is missing a parameter that is essential")
            raise HTTPNotFound()

        proj_id = self.request.params['proj_id']
        description = self.request.params["description"]

        # Verifies that the project id exists
        proj_type = self.context.verifyProjectId(proj_id)
        if proj_type is None:
            log.warning("project does not exist")
            raise HTTPNotFound()

        if "user_id" not in session or "username" not in session:
            log.warning("user_id not found in session")
            raise HTTPBadRequest()

        user_id = session["user_id"]

        # Verifies that only the owner of the web page can initiate an edit of their project description
        proj_type = self.context.verifyProjectOwner(proj_id, session["username"])
        if proj_type is None:
            log.warning("session username does not match the project owner")
            raise HTTPForbidden()
        
        self.context.changeProjectDescription(proj_id, description)
        json_hash = {'result': '0'}
        json_dump = json.dumps(json_hash)
        log.debug("json dump = %s" % json_dump)

        return Response(json_dump)    

        
