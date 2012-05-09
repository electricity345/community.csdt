import json
import logging

from community_csdt.src.models import database

class Gallery(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Gallery.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Returns the number of classes that are active
    def getNumOfAllActiveClasses(self):
        log = logging.getLogger('csdt')
        log.info("Gallery.getNumOfAllActiveClasses()")
   
        sql = "SELECT COUNT(DISTINCT cm.class_id) AS num_classes FROM class_memberships cm, classnames cn, classrooms c, users u WHERE cm.permissions = \'t\' AND c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND c.active = 1 AND u.active = 1;"
        result = database.executeSelectQuery(sql, "one")

        return result["num_classes"]

    # Returns a list of all classrooms that are available for a user to join. Classroom has to be active. (Visible?)
    def getAllActiveClasses(self, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Gallery.getAllActiveClasses()")

        sql = "SELECT table_B.class_id AS cid, table_B.classname AS classname, COUNT(cm.user_id) AS size, table_B.username AS username, table_B.first_name AS first_name, table_B.last_name AS last_name FROM (SELECT table_A.class_id AS class_id, table_A.classname AS classname, table_A.username AS username, table_A.first_name AS first_name, table_A.last_name AS last_name, cm.user_id AS user_id, table_A.permissions AS permissions FROM (SELECT cn.class_id AS class_id, cn.classname AS classname, un.username AS username, u.first_name AS first_name, u.last_name AS last_name, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, usernames un, users u WHERE cm.permissions = \'t\' AND c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND u.id = un.user_id AND c.active = 1 AND u.active = 1) table_A, class_memberships cm, users u WHERE u.active = 1 AND table_A.class_id = cm.class_id AND cm.user_id = u.id) table_B LEFT JOIN class_memberships cm ON table_B.class_id = cm.class_id AND table_B.permissions <> cm.permissions AND table_B.user_id = cm.user_id GROUP BY table_B.class_id ORDER BY %s %s;" % (sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["cid"]
            class_hash['classname'] = row["classname"]
            class_hash['size'] = row["size"]
            class_hash['username'] = row["username"]
            class_hash['first_name'] = row["first_name"]
            class_hash['last_name'] = row["last_name"]
            class_hash['full_name'] = class_hash['first_name'] + " " + class_hash['last_name']
            class_list.append(class_hash)
    
        return class_list


