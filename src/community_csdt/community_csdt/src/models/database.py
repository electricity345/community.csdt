import json
import logging
import MySQLdb

class Database():
    def __init__(self):
        self.conn = ""

    def connect(self):
        self.conn = MySQLdb.connect(db="community", user="community", passwd="12345", host="localhost")

    def commit(self):
        self.conn.commit() # Make the changes to the database persistent

    def query(self, query_str):
        log = logging.getLogger('csdt')
        log.info("Database.query()")

        try:
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query_str)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query_str)

        return cur
        
db = Database() # create database object

def executeSelectQuery(query_str, fetch_type):
    log = logging.getLogger('csdt')
    log.info("Database.executeSelectQuery()")
    log.debug("query str = %s" % query_str)

    cur = db.query(query_str)

    result = None
    if fetch_type == "one":
        result = cur.fetchone()
    elif fetch_type == "many":
        result = cur.fetchall()
        
    if result is None:
        log.warning("Query returns no result")
        return result

    return result

def executeUpdateQuery(query_str):
    log = logging.getLogger('csdt')
    log.info("Database.executeUpdateQuery()")
    log.debug("query str = %s" % query_str)

    cur = db.query(query_str)

    db.commit() # Make the changes to the database persistent
    return

def executeInsertQuery(query_str):
    log = logging.getLogger('csdt')
    log.info("Database.executeInsertQuery()")
    log.debug("query str = %s" % query_str)

    cur = db.query(query_str)

    db.commit() # Make the changes to the database persistent
    return cur.lastrowid

def executeDeleteQuery(query_str):
    log = logging.getLogger('csdt')
    log.info("Database.executeDeleteQuery()")
    log.debug("query str = %s" % query_str)

    cur = db.query(query_str)

    db.commit() # Make the changes to the database persistent
    return


