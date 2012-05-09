import ezPyCrypto
import json
import logging
import os
import random
import smtplib
import tinyurl
import unicodedata
import urllib

from email.mime.text import MIMEText
from community_csdt.src.models import database

class Recover(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("Recover.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Checks if username already exists in database and is currently active.
    def doesUsernameExist(self, username):
        log = logging.getLogger('csdt')
        log.info("Recover.doesUsernameExist()")
  
        sql = "SELECT un.user_id AS user_id FROM usernames un, users u WHERE un.user_id = u.id AND un.username = \'%s\' AND u.active = 1;" % (str(username))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return
        
        return result["user_id"]

    # Returns the username, first name, last name, email, and about me information of a user given their user_id
    def getUserProfileInformation(self, user_id):
        log = logging.getLogger('csdt')
        log.info("Recover.getUserProfileInformation()")
    
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

    # Increments the reset_pass_counter by 1 for the specified user
    def updateResetPasswordCounter(self, user_id, reset_pass_counter): 
        log = logging.getLogger('csdt')
        log.info("Recover.updateResetPasswordCounter()")

        reset_pass_counter += 1 # Increment the reset password counter by 1
   
        sql = "UPDATE users SET reset_pass_counter = %s WHERE id = %s;" % (str(reset_pass_counter), str(user_id))
        result = database.executeUpdateQuery(sql)

        return reset_pass_counter

    # Encrypts the input string by appending it with a nonce in front and then encrypting it with ezPyCrypto's default algorithm
    def encryptUrlQuery(self, plain_string):
        log = logging.getLogger('csdt')
        log.info("Recover.encryptUrlQuery()")

        # Create a nonce
        nonce = random.randint(1, 4000000000)
        log.debug("nonce = %d" % nonce)

        # Appends nonce to beginning of plaintext and has the ";" as the deliminator
        plaintext = str(nonce) + ";" + plain_string
        log.debug("plaintext = %s" % plaintext)

        key = ezPyCrypto.key(1024)

        # Path = ../../../../email_key.pub
        path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'email_key.pub')
        fd = open(path, "rb")
        public_key = fd.read()
        fd.close()

        key.importKey(public_key)

        plaintext_ascii = unicodedata.normalize('NFKD', plaintext).encode('ascii', 'ignore')
        ciphertext = key.encStringToAscii(plaintext_ascii)

        return ciphertext

    # Creates the url for a user to recover and change their old password
    def createAccountRecoveryUrl(self, host_url, ciphertext):
        log = logging.getLogger('csdt')
        log.info("Recover.createAccountRecoveryUrl()")    

        url = host_url + "/recover/account" + "?value=" + urllib.quote(ciphertext)
        log.debug("url = %s" % url)
        #tiny_url = tinyurl.create_one(url)
        tiny_url = url
        log.debug("tinyurl = %s" % tiny_url)

        return tiny_url

    # Creates an account recovery letter for a particular user
    def createAccountRecoveryLetter(self, host_url, username, email, ciphertext):
        log = logging.getLogger('csdt')
        log.info("Recover.createAccountRecoveryLetter()")    

        url = self.createAccountRecoveryUrl(host_url, ciphertext)
        body = "Reset CSDT Community Password\n\n" + "To reset your password for your account: " + username + ", use the following link:\n" + url + "\n\n" + "This message was sent to protect the account of" + email +  "on CSDT Community." + "If you have received this message in error, or wish to report abuse, please contact us at csdt.community@gmail.com.\n"
        log.debug("Body = %s" % body) 

        msg = MIMEText(body)
        msg["From"] = "no-reply@rpi.edu"
        log.debug("FROM = %s" % msg["From"])
        msg["To"] = email
        log.debug("To = %s" % msg["To"])
        msg["Subject"] = "CSDT Community: Confirm Your Account"
        log.debug("Subject = %s" % msg["Subject"])
    
        log.debug("Email = " + msg.as_string())
        #mail_server = smtplib.SMTP('localhost')
        #mail_server.set_debuglevel(1)
        #mail_server.ehlo()
        #mail_server.starttls()
        #mail_server.ehlo()
        #mail_server.sendmail(msg["From"], msg["To"], msg.as_string())
        #mail_server.quit()
        #log.debug("email has been sent...")
    
        return

    # Checks if email already exists in database and is currently active.
    def doesEmailExist(self, email):
        log = logging.getLogger('csdt')
        log.info("Recover.doesEmailExist()")
 
        sql = "SELECT id AS user_id FROM users WHERE email = \'%s\' AND active = 1;" % (str(email))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return
        
        return result["user_id"]

    # Decrypts the ciphertext with ezPyCrypto's default algorithm
    def decryptUrlQuery(self, ciphertext):
        log = logging.getLogger('csdt')
        log.info("Recover.decryptUrlQuery()")

        # Path = ../../../../email_key.priv
        path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'email_key.priv')
        fd = open(path, "rb")
        private_key = fd.read()
        fd.close()

        key = ezPyCrypto.key(private_key)

        try:
            plaintext = key.decStringFromAscii(ciphertext)
        except:
            plaintext = ""        

        return plaintext

    # Returns a list of all classrooms that a single user (teacher) manages. Classrooms have to be active and public or privately viewable.
    def getAllClassesEnrolledAsTeacher(self, user_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Recover.getAllClassesEnrolledAsTeacher()")

        sql = "SELECT table_B.class_id AS class_id, table_B.classname AS classname, COUNT(cm.user_id) AS size FROM (SELECT table_A.class_id AS class_id, table_A.classname AS classname, cm.user_id AS user_id, table_A.permissions AS permissions FROM (SELECT cn.class_id AS class_id, cn.classname AS classname, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND cm.user_id = %s AND cm.permissions = \'t\' AND c.active = 1 AND u.active = 1) table_A, class_memberships cm, users u WHERE u.active = 1 AND table_A.class_id = cm.class_id AND cm.user_id = u.id) table_B LEFT JOIN class_memberships cm ON table_B.class_id = cm.class_id AND table_B.permissions <> cm.permissions AND table_B.user_id = cm.user_id GROUP BY table_B.class_id ORDER BY %s %s;" % (str(user_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")
        if result is None:
            log.warning("teacher does not exist")
            return

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["class_id"]
            class_hash['classname'] = row["classname"]
            class_hash['size'] = row["size"]           
            class_list.append(class_hash)

        return class_list

    # Returns a list of all classrooms that a single user is enrolled in. Classrooms have to be active and public or privately viewable. 
    def getAllClassesEnrolledAsStudent(self, user_id, sort_name, sort_order):
        log = logging.getLogger('csdt')
        log.info("Recover.getAllClassesEnrolledAsStudent()")

        sql = "SELECT table_B.class_id AS class_id, table_B.classname AS classname, COUNT(cm.user_id) AS size, table_B.username AS username, table_B.first_name AS first_name, table_B.last_name AS last_name FROM (SELECT table_A.class_id AS class_id, table_A.classname AS classname, un.username AS username, u.first_name AS first_name, u.last_name AS last_name, cm.user_id AS user_id, table_A.permissions AS own_permissions FROM (SELECT cn.class_id AS class_id, cn.classname AS classname, cm.permissions AS permissions FROM classnames cn, class_memberships cm, classrooms c, users u WHERE c.id = cn.class_id AND cn.class_id = cm.class_id AND cm.user_id = u.id AND cm.user_id = %s AND cm.permissions = 's' AND c.active = 1 AND u.active = 1) table_A, class_memberships cm, usernames un, users u WHERE table_A.class_id = cm.class_id AND cm.user_id = u.id AND u.id = un.user_id AND u.active = 1) table_B LEFT JOIN class_memberships cm ON table_B.class_id = cm.class_id AND table_B.own_permissions = cm.permissions AND table_B.user_id = cm.user_id GROUP BY table_B.class_id ORDER BY %s %s;" % (str(user_id), sort_name, sort_order)
        result = database.executeSelectQuery(sql, "many")
        if result is None:
            log.warning("user does not exist")
            return

        class_list = []
        for row in result:
            class_hash = {}
            class_hash['cid'] = row["class_id"]
            class_hash['classname'] = row["classname"]
            class_hash['size'] = row["size"]
            class_hash['username'] = row["username"]
            class_hash['first_name'] = row["first_name"]
            class_hash['last_name'] = row["last_name"]
            class_hash['full_name'] = class_hash["first_name"] + " " + class_hash["last_name"]
            class_list.append(class_hash)

        return class_list

    # Changes the password of a user
    def changeUserPassword(self, user_id, password): 
        log = logging.getLogger('csdt')
        log.info("Recover.changeUserPassword()")
 
        # Changes the password for the user
        sql = "UPDATE usernames SET pass = \'%s\' WHERE user_id = %s;" % (str(password), str(user_id))
        result = database.executeUpdateQuery(sql)

        # Resets password flag to 0 for the user
        sql = "UPDATE users SET reset_pass = 0 WHERE id = %s;" % (str(user_id))
        result = database.executeUpdateQuery(sql)

        return


