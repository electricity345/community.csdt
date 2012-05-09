import json
import logging

from community_csdt.src.models import database
from community_csdt.src.models.projects import project_comment
from community_csdt.src.utils import date

class Project(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Project.__getitem__()")
        log.debug("key = %s" % key)
    
        if key == "comments":
            return project_comment.ProjectComment(self, key)

        raise KeyError

    # Returns the number of projects uploaded by all users that are both active and publically viewable
    def getSizeOfActiveProjectTable(self):
        log = logging.getLogger('csdt')
        log.info("Project.getSizeOfActiveProjectTable()")

        sql = "SELECT COUNT(id) AS size FROM projects WHERE visible = 1 AND active = 1;"
        result = database.executeSelectQuery(sql, "one")

        return result["size"]

    # Returns a list of all projects uploaded by all users that are both active and publically viewable  
    def getActiveProjectTable(self, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Project.getActiveProjectTable()")

        sql = "SELECT table_A.proj_id AS id, table_A.username AS username, table_A.proj_name AS proj_name, table_A.proj_type AS proj_type, table_A.description AS description, table_A.num_views AS num_views, COUNT(table_B.rating) AS ratings, table_A.downloads AS downloads, table_A.stored_proj_name as stored_proj_name, table_A.time AS time FROM (SELECT p.id AS proj_id, u.id AS user_id, un.username AS username, p.proj_name AS proj_name, p.proj_type AS proj_type, p.description AS description, p.num_views AS num_views, p.downloads AS downloads, p.stored_proj_name AS stored_proj_name, p.time AS time FROM projects p, users u, usernames un WHERE p.user_id = u.id AND u.id = un.user_id AND p.visible = 1 AND p.active = 1) table_A LEFT JOIN (SELECT pr.project_id, pr.rating FROM project_ratings pr, users u WHERE u.id = pr.user_id AND u.active = 1) table_B ON table_B.project_id = table_A.proj_id GROUP BY table_A.proj_id ORDER BY %s %s;" % (sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        proj_list = []
        for row in result:
            proj_hash = {}
            date_obj = date.date()
            proj_hash['id'] = row["id"]
            proj_hash['username'] = row["username"]
            proj_hash['proj_name'] = row["proj_name"]
            proj_hash['proj_type'] = row["proj_type"]
            proj_hash['description'] = row["description"]
            proj_hash['num_views'] = row["num_views"]
            proj_hash['ratings'] = row["ratings"]
            proj_hash['downloads'] = row["downloads"]
            proj_hash['stored_proj_name'] = row["stored_proj_name"]
            proj_hash['time'] = date_obj.modifyDate(row["time"])
            proj_list.append(proj_hash)
    
        return proj_list

    # Verifies whether or not the project id exists. Returns the project type of the project if it exists. Otherwise, it returns None.
    def verifyProjectId(self, proj_id):
        log = logging.getLogger('csdt')
        log.info("Project.verifyProjectId()")

        sql = "SELECT p.proj_type AS proj_type FROM projects p, users u WHERE p.user_id = u.id AND p.id = %s AND p.active = 1 AND u.active = 1;" % (str(proj_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("project does not exist")
            return

        return result["proj_type"]

    # Verifies if a user is the owner of a specific project. Returns the project type if the user owns the specific project. Otherwise, it returns None.
    def verifyProjectOwner(self, proj_id, username):
        log = logging.getLogger('csdt')
        log.info("Project.verifyProjectOwner()")

        sql = "SELECT p.proj_type AS proj_type FROM projects p, users u, usernames un WHERE p.user_id = u.id AND u.id = un.user_id AND p.id = %s AND un.username = '%s' AND p.active = 1 AND u.active = 1;" % (str(proj_id), str(username))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("project does not exist")
            return

        return result["proj_type"]

    # Returns info about a single project given a project id, regardless of being public or privately viewable. Project has to be active.
    def getSingleProject(self, proj_id):
        log = logging.getLogger('csdt')
        log.info("Project.getSingleProject()")
        
        sql = "SELECT table_A.proj_id AS proj_id, table_A.username AS username, table_A.proj_name AS proj_name, table_A.proj_type AS proj_type, table_A.description AS description, table_A.num_views AS num_views, COUNT(table_B.rating) AS ratings, table_A.downloads AS downloads, table_A.stored_proj_name AS stored_proj_name, table_A.time AS time FROM (SELECT p.id AS proj_id, u.id AS user_id, un.username AS username, p.proj_name AS proj_name, p.proj_type AS proj_type, p.description AS description, p.num_views AS num_views, p.downloads AS downloads, p.stored_proj_name AS stored_proj_name, p.time AS time FROM projects p, users u, usernames un WHERE p.user_id = u.id AND u.id = un.user_id AND p.id = %s AND p.active = 1) table_A LEFT JOIN (SELECT pr.project_id, pr.rating FROM project_ratings pr, users u WHERE u.id = pr.user_id AND u.active = 1) table_B ON table_B.project_id = table_A.proj_id GROUP BY table_A.proj_id;" % (str(proj_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("project does not exist")
            return

        proj_info = {}
        proj_info["proj_id"] = result["proj_id"]
        proj_info["username"] = result["username"]
        proj_info["proj_name"] = result["proj_name"]
        proj_info["proj_type"] = result["proj_type"]
        proj_info["description"] = result["description"]
        proj_info["num_views"] = result["num_views"]
        proj_info["ratings"] = result["ratings"]
        proj_info["downloads"] = result["downloads"]        
        proj_info["stored_proj_name"] = result["stored_proj_name"]
        proj_info["time"] = result["time"]   

        return proj_info

    # Increments the number of views for the specified project by 1
    def incrementViewCount(self, proj_id): 
        log = logging.getLogger('csdt')
        log.info("Project.incrementViewCount()")

        # Updates the number of views for the specified project by 1
        sql = "UPDATE projects SET num_views = num_views + 1 WHERE id = %s;" % (str(proj_id))
        result = database.executeUpdateQuery(sql)

        return

    # Gets the project owner given the project id
    def getProjectOwner(self, proj_id):
        log = logging.getLogger('csdt')
        log.info("Project.getProjectOwner()")

        sql = "SELECT user_id FROM projects WHERE id = %s;" % (str(proj_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("project does not exist")
            return

        return result["user_id"]

    # Returns the average user rating and the number of reviews for a given project. Project has to be active.
    # Returns 0 for both rating and reviews if there are no entries.
    def getAvgProjRating(self, proj_id):
        log = logging.getLogger('csdt')
        log.info("Project.getAvgProjRating()")
    
        sql = "SELECT AVG(pr.rating) AS average_ratings, COUNT(pr.rating) AS num_reviews FROM projects p, project_ratings pr, users u WHERE p.id = pr.project_id AND u.id = pr.user_id AND pr.project_id = %s AND u.active = 1 AND p.active = 1 GROUP BY pr.project_id;" % (str(proj_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("project does not have a rating")
            ratings = {}
            ratings["average_ratings"] = 0
            ratings["num_reviews"] = 0
            return ratings

        ratings = {}        
        ratings["average_ratings"] = result["average_ratings"]
        ratings["num_reviews"] = result["num_reviews"]

        return ratings

    # Adds a user's rating for a given project. Project has to be active.
    def addProjectRating(self, proj_id, user_id, rating):
        log = logging.getLogger('csdt')
        log.info("Project.addProjectRating()")

        # Checks if user has already submitted a rating to the given project. If not, it should return an empty set.
        sql = "SELECT pr.project_id AS project_id, pr.user_id AS user_id, pr.rating AS rating from projects p, project_ratings pr, users u WHERE p.id = pr.project_id AND u.id = pr.user_id AND pr.project_id = %s AND pr.user_id = %s AND u.active = 1 AND p.active = 1;" % (str(proj_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            if int(rating) == 0:
                log.warning("User has returned a 0 rating")
                return

            sql = "INSERT INTO project_ratings (project_id, user_id, rating) VALUES (%s, %s, %s);" % (str(proj_id), str(user_id), str(rating))
            result = database.executeInsertQuery(sql)
            return

        sql = "DELETE FROM project_ratings where project_id = %s AND user_id = %s;" % (str(proj_id), str(user_id))
        result = database.executeDeleteQuery(sql)

        if int(rating) == 0:
            log.warning("User has returned a 0 rating")
            return

        sql = "INSERT INTO project_ratings (project_id, user_id, rating) VALUES (%s, %s, %s);" % (str(proj_id), str(user_id), str(rating))
        result = database.executeInsertQuery(sql)

        return

    # Returns the project rating for a project rated by a given user. Project has to be active.
    def getProjRatingForAUser(self, proj_id, user_id):
        log = logging.getLogger('csdt')
        log.info("Project.getProjRatingForAUser()")
    
        sql = "SELECT pr.rating AS rating from projects p, project_ratings pr, users u WHERE p.id = pr.project_id AND u.id = pr.user_id AND pr.project_id = %s AND pr.user_id = %s AND u.active = 1 AND p.active = 1;" % (str(proj_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user has not submitted a rating for the particular project")
            return

        return result["rating"]

    # Changes the description of a project given their proj_id.
    def changeProjectDescription(self, proj_id, description): 
        log = logging.getLogger('csdt')
        log.info("Project.changeProjectDescription()")
   
        # Updates the project description for the specified project
        sql = "UPDATE projects SET description = '%s' WHERE id = %s;" % (str(description), str(proj_id))
        result = database.executeUpdateQuery(sql)

        return

     
