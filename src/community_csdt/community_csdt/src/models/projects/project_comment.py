import json
import logging

from community_csdt.src.models import database
from community_csdt.src.utils import date

class ProjectComment(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("ProjectComment.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Adds a new comment to a specific project.
    def addProjectComment(self, proj_id, user_id, text): 
        log = logging.getLogger('csdt')
        log.info("ProjectComment.addProjectComment()")

        # Inserts a new comment for the specified project
        sql = "INSERT INTO project_comments (user_id, project_id, text) VALUES (%s, %s, '%s');" % (str(user_id), str(proj_id), str(text))
        comment_id = database.executeInsertQuery(sql)

        # Determines if the project is associated with any classes and if so, determines the flag comment level of those classes
        sql = "SELECT c.id AS class_id, c.owner AS owner, c.flag_comment_level AS flag_comment_level FROM classrooms c, project_memberships pm WHERE pm.class_id = c.id AND pm.project_id = %s;" % (str(proj_id))
        result = database.executeSelectQuery(sql, "many")
        if result is None:
            log.warning("project is not associated with a class")
            return

        # Checks to see if the flag comment level of a class is set to 2, which indicates that the class teacher wants to monitor all comments. 
        # Thus, we will flag that comment
        flag = 0
        for row in result:
            if row["flag_comment_level"] != 2:
                continue

            sql = "INSERT INTO project_comments_ratings (proj_comment_id, user_id, flag) VALUES (%s, %s, 1);" % (str(comment_id), str(row["owner"]))
            value = database.executeInsertQuery(sql)
            flag = 1

        if flag == 1:
            sql = "UPDATE project_comments SET flag = 1 WHERE id = %s;" % (str(comment_id))
            result = database.executeUpdateQuery(sql)

        return

    # Returns all comments for a specific project. Project has to be active.
    def getCommentsForAProject(self, proj_id):
        log = logging.getLogger('csdt')
        log.info("ProjectComment.getCommentsForAProject()")
    
        sql = "SELECT table_A.proj_comment_id AS id, table_A.username AS username, table_A.text AS text, table_A.time AS time, SUM(table_B.rating) AS ratings, table_A.flag AS flag FROM (SELECT un.username AS username, pc.id AS proj_comment_id, pc.text AS text, pc.flag AS flag, pc.time AS time FROM project_comments pc, usernames un WHERE pc.user_id = un.user_id AND pc.active = 1 AND pc.project_id = %s) table_A LEFT JOIN (SELECT pcr.proj_comment_id AS proj_comment_id, pcr.user_id AS user_id, pcr.rating AS rating FROM project_comments pc, project_comments_ratings pcr WHERE pc.id = pcr.proj_comment_id AND pc.active = 1 AND pc.project_id = %s) table_B ON table_A.proj_comment_id = table_B.proj_comment_id GROUP BY table_A.proj_comment_id ORDER BY table_A.time ASC;" % (str(proj_id), str(proj_id))
        result = database.executeSelectQuery(sql, "many")
        if result is None:
            log.warning("comments do not exist for project")
            return

        comment_list = []
        for row in result:
            comment_hash = {}
            date_obj = date.date()
            comment_hash['id'] = row["id"]
            comment_hash['username'] = row["username"]
            comment_hash['text'] = row["text"]
            comment_hash['time'] = date_obj.modifyDate(row["time"])
            if row["ratings"] is None:
                comment_hash['ratings'] = 0
            else:
                comment_hash['ratings'] = int(row["ratings"])

            comment_hash['flag'] = int(row["flag"])
            comment_list.append(comment_hash)

        return comment_list

    # Sets the flag for the specified comment
    def setProjectCommentFlag(self, comment_id, user_id): 
        log = logging.getLogger('csdt')
        log.info("ProjectComment.setCommentFlag()")
      
        # Sets the flag for the specified comment
        sql = "UPDATE project_comments SET flag = 1 WHERE id = %s AND active = 1;" % (str(comment_id))
        result = database.executeUpdateQuery(sql)

        # Checks if user has already submited a rating score for the specified comment
        sql = "SELECT COUNT(user_id) AS exist FROM project_comments_ratings WHERE proj_comment_id = %s AND user_id = %s;" % (str(comment_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result["exist"] == 1:
            # Sets the flag for the specified comment
            sql = "UPDATE project_comments_ratings SET flag = 1 WHERE proj_comment_id = %s AND user_id = %s;" % (str(comment_id), str(user_id))
            result = database.executeUpdateQuery(sql)
        else:
            # Inserts the flag for the specified comment
            sql = "INSERT INTO project_comments_ratings (proj_comment_id, user_id, flag) VALUES (%s, %s, 1);" % (str(comment_id), str(user_id))
            result = database.executeInsertQuery(sql)

        return 

    # Rates a specific comment in a specific project. Returns 1 if user has already submitted a rating for the specific comment. Otherwise it returns None.
    def addProjectCommentRating(self, comment_id, user_id, rating): 
        log = logging.getLogger('csdt')
        log.info("ProjectComment.addProjectCommentRating()")
     
        # Checks if user has already submited a rating score for a specific comment in a specific project
        sql = "SELECT COUNT(proj_comment_id) AS exist FROM project_comments_ratings WHERE proj_comment_id = %s AND user_id = %s AND rating = %s;" % (str(comment_id), str(user_id), str(rating))
        result = database.executeSelectQuery(sql, "one")
        if result["exist"] == 1:
            return 1

        # Inserts a rating score for a specific comment in a specific project 
        sql = "INSERT INTO project_comments_ratings (proj_comment_id, user_id, rating) VALUES (%s, %s, %s);" % (str(comment_id), str(user_id), str(rating))
        result = database.executeInsertQuery(sql)
      
        return

    # Verifies whether or not the project id exists. Returns the project type of the project if it exists. Otherwise, it returns None.
    def verifyProjectId(self, proj_id):
        log = logging.getLogger('csdt')
        log.info("ProjectComment.verifyProjectId()")

        sql = "SELECT p.proj_type AS proj_type FROM projects p, users u WHERE p.user_id = u.id AND p.id = %s AND p.active = 1 AND u.active = 1;" % (str(proj_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("project does not exist")
            return

        return result["proj_type"]


