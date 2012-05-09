import json
import logging

from community_csdt.src.models import database
from community_csdt.src.utils import date

class AccountComment(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self.owner = self.__parent__.owner
        self.user_id = self.__parent__.user_id

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("AccountComment.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Returns the number of comments that are flagged for a teacher, regardless of being public or privately viewable. Projects have to be active.
    def getNumOfFlaggedComments(self, user_id):
        log = logging.getLogger('csdt')
        log.info("AccountComment.getNumOfFlaggedComments()")
    
        sql = "SELECT COUNT(table_A.flag) AS num_comments FROM (SELECT p.id AS project_id, pc.flag AS flag FROM projects p, project_comments pc WHERE p.id = pc.project_id AND p.active = 1 AND pc.flag = 1) table_A RIGHT JOIN (SELECT DISTINCT pm.project_id AS project_id FROM class_memberships cm, project_memberships pm WHERE cm.class_id = pm.class_id AND cm.user_id = %s AND cm.permissions = 't') table_B ON table_A.project_id = table_B.project_id;" % (str(user_id))
        result = database.executeSelectQuery(sql, "one")

        return result["num_comments"]

    # Returns all comments for a specific project. Project has to be active.
    def getAllFlaggedCommentsForATeacher(self, user_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("AccountComment.getAllFlaggedCommentsForATeacher()")
    
        sql = "SELECT table_A.proj_comment_id AS proj_comment_id, table_A.comment_owner AS comment_owner, table_A.proj_name AS proj_name, table_A.text AS text, table_A.time AS time FROM (SELECT p.id AS project_id, pc.id AS proj_comment_id, un.username AS comment_owner, p.proj_name AS proj_name, pc.text AS text, pc.time AS time FROM projects p, project_comments pc, usernames un WHERE p.id = pc.project_id AND p.user_id = un.user_id AND p.active = 1 AND pc.flag = 1) table_A RIGHT JOIN (SELECT DISTINCT pm.project_id AS project_id FROM class_memberships cm, project_memberships pm WHERE cm.class_id = pm.class_id AND cm.user_id = %s AND cm.permissions = 't') table_B ON table_A.project_id = table_B.project_id ORDER BY %s %s;" % (str(user_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        comment_list = []
        for row in result:
            comment_hash = {}
            date_obj = date.date()
            comment_hash['proj_comment_id'] = row["proj_comment_id"]
            comment_hash['comment_owner'] = row["comment_owner"]
            comment_hash['proj_name'] = row["proj_name"]
            comment_hash['text'] = row["text"]
            comment_hash['time'] = date_obj.modifyDate(row["time"])
            comment_list.append(comment_hash)
    
        return comment_list

    # Verifies whether or not the comment is under the jurisdiction of the teacher to moderate. Returns the project comment id if it is verified.
    def verifyCommentId(self, comment_id, user_id):
        log = logging.getLogger('csdt')
        log.info("AccountComment.verifyCommentId()")
    
        sql = "SELECT pc.id AS proj_comment_id FROM class_memberships cm, projects p, project_comments pc, project_memberships pm WHERE cm.class_id = pm.class_id AND pm.project_id = pc.project_id AND pm.project_id = p.id AND pc.id = %s AND cm.user_id = %s AND cm.permissions = 't';" % (str(comment_id), str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("comment is not under the jurisdication of the user")
            return

        return result["proj_comment_id"]

    # Approves a particular comment after it has been flagged
    def approveComment(self, comment_id): 
        log = logging.getLogger('csdt')
        log.info("AccountComment.approveComment()")
    
        # Removes the flag for the specified comment
        sql = "UPDATE project_comments SET flag = 0 WHERE id = %s;" % (str(comment_id))
        result = database.executeUpdateQuery(sql)

        # Removes the flag for all users who flagged the specific comment
        sql = "UPDATE project_comments_ratings SET flag = 0 WHERE proj_comment_id = %s;" % (str(comment_id))
        result = database.executeUpdateQuery(sql)

        return 

    # Bans a particular comment after it has been flagged
    def banComment(self, comment_id): 
        log = logging.getLogger('csdt')
        log.info("AccountComment.banComment()")

        # Removes the flag and the comment
        sql = "UPDATE project_comments SET flag = 0, active = 0 WHERE id = %s;" % (str(comment_id))
        result = database.executeUpdateQuery(sql)

        # Removes the flag for all users who flagged the specific comment
        sql = "DELETE FROM project_comments_ratings WHERE proj_comment_id = %s;" % (str(comment_id))
        result = database.executeDeleteQuery(sql)
        
        return 

    # Returns the number of users who flagged a particular comment
    def getNumOfFlaggedCommentUsers(self, comment_id):
        log = logging.getLogger('csdt')
        log.info("AccountComment.getNumOfFlaggedCommentUsers()")
    
        sql = "SELECT COUNT(pcr.user_id) AS num_users FROM project_comments_ratings pcr WHERE pcr.proj_comment_id = %s AND pcr.flag = 1;" % (str(comment_id))
        result = database.executeSelectQuery(sql, "one")

        return result["num_users"]

    # Returns the usernames of all the users who flagged a particular comment
    def getFlaggedCommentUsers(self, comment_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("AccountComment.getFlaggedCommentUsers()")
    
        sql = "SELECT u.username AS username FROM project_comments_ratings pcr, usernames u WHERE pcr.user_id = u.user_id AND pcr.proj_comment_id = %s AND pcr.flag = 1 ORDER BY %s %s;" % (str(comment_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        comment_list = []
        for row in result:
            comment_hash = {}
            comment_hash['username'] = row["username"]
            comment_list.append(comment_hash)
    
        return comment_list


