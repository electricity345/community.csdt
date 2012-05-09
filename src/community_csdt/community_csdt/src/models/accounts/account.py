import json
import logging

from community_csdt.src.models import database
from community_csdt.src.models.accounts import account_admin
from community_csdt.src.utils import date

class Account(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name
        self.owner = ""
        self.user_id = ""

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Account.__getitem__()")
        log.debug("key = %s" % key)

        if key == "admin":
            return account_admin.AccountAdmin(self, key)

        user_id = self.getUserId(key)
        if user_id is None:
            raise KeyError

        self.owner = key
        self.user_id = int(user_id)

        return self

    # Returns the corresponding user_id of a given username 
    def getUserId(self, username):
        log = logging.getLogger('csdt')
        log.info("Account.getUserId()")
    
        sql = "SELECT u.id AS user_id FROM users u, usernames un WHERE u.id = un.user_id AND un.username = \'%s\' AND u.active = 1;" % (username)
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return

        user_id = result["user_id"]

        log.debug("user_id = %s" % user_id)
        return user_id

    # Returns the username, first name, last name, email, and about me information of a user given their user_id
    def getUserProfileInformation(self, user_id):
        log = logging.getLogger('csdt')
        log.info("Account.getUserProfileInformation()")
    
        sql = "SELECT un.username AS username, u.first_name AS first_name, u.last_name AS last_name, u.email AS email, u.permissions AS permissions, u.reset_pass AS reset_pass, u.reset_pass_counter AS reset_pass_counter, up.about AS about FROM usernames un, user_profile up, users u WHERE u.id = %s AND u.id = un.user_id AND u.id = up.user_id AND u.active = 1;" % (str(user_id))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return

        user_info = {}
        user_info["username"] = result["username"]
        user_info["first_name"] = result["first_name"]
        user_info["last_name"] = result["last_name"]
        user_info["email"] = result["email"]
        user_info["permissions"] = result["permissions"]
        user_info["reset_pass"] = result["reset_pass"]
        user_info["reset_pass_counter"] = result["reset_pass_counter"]
        user_info["about"] = result["about"]

        return user_info

    # Returns the number of projects that a specific user has, regardless of being public or privately viewable. Projects have to be active.
    def getSizeOfActiveProjectTableForAUser(self, user_id):
        log = logging.getLogger('csdt')
        log.info("Account.getSizeOfActiveProjectTableForAUser()")
       
        sql = "SELECT COUNT(id) AS size FROM projects WHERE user_id = %s AND active = 1;" % (str(user_id))
        result = database.executeSelectQuery(sql, "one")

        return result["size"]

    # Returns a list of projects that a specific user has uploaded, regardless of being public or privately viewable. Projects have to be active.
    def getActiveProjectTableForAUser(self, user_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Account.getActiveProjectTableForAUser()")
    
        sql = "SELECT table_A.proj_id AS id, table_A.username AS username, table_A.proj_name AS proj_name, table_A.proj_type AS proj_type, table_A.description AS description, table_A.num_views AS num_views, COUNT(table_B.rating) AS ratings, table_A.downloads AS downloads, table_A.stored_proj_name AS stored_proj_name, table_A.time AS time FROM (SELECT p.id AS proj_id, u.id AS user_id, un.username AS username, p.proj_name AS proj_name, p.proj_type AS proj_type, p.description AS description, p.num_views AS num_views, p.downloads AS downloads, p.stored_proj_name AS stored_proj_name, p.time AS time FROM projects p, users u, usernames un WHERE p.user_id = u.id AND u.id = un.user_id AND u.id = %s AND p.active = 1) table_A LEFT JOIN (SELECT pr.project_id, pr.rating FROM project_ratings pr, users u WHERE u.id = pr.user_id AND u.active = 1) table_B ON table_B.project_id = table_A.proj_id GROUP BY table_A.proj_id ORDER BY %s %s;" % (str(user_id), sort_name, sort_order)
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


