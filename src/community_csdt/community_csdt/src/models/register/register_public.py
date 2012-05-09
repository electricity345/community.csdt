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

class RegisterPublic(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.__getitem__()")
        log.debug("key = %s" % key)

        raise KeyError

    # Checks if username already exists in database and is currently active.
    def doesUsernameExist(self, username):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.doesUsernameExist()")
  
        sql = "SELECT un.user_id AS user_id FROM usernames un, users u WHERE un.user_id = u.id AND un.username = \'%s\' AND u.active = 1;" % (str(username))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return
        
        return result["user_id"]

    # Checks if email already exists in database and is currently active.
    def doesEmailExist(self, email):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.doesEmailExist()")
 
        sql = "SELECT id AS user_id FROM users WHERE email = \'%s\' AND active = 1;" % (str(email))
        result = database.executeSelectQuery(sql, "one")
        if result is None:
            log.warning("user does not exist")
            return
        
        return result["user_id"]

    # Encrypts the input string by appending it with a nonce in front and then encrypting it with ezPyCrypto's default algorithm
    def encryptUrlQuery(self, plain_string):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.encryptUrlQuery()")

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

    # Creates a confirmation letter to the new user who registered
    def createConfirmationLetter(self, host_url, email, first_name, last_name, ciphertext):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.createConfirmationLetter()")    

        url = host_url + "/register/accounts/public/new" + "?value=" + urllib.quote(ciphertext)
        log.debug("url = %s" % url)
        #tiny_url = tinyurl.create_one(url)
        tiny_url = url
        log.debug("tinyurl = %s" % tiny_url)

        body = "Dear " + first_name + " " + last_name + ",\n\n" + "Thanks for registering. In order to activate your account, you must complete one more step.\n\n" + "Please note: you must complete the last step to become a registered member. You will only need to visit this link ONCE to activate your account.\n\n" +"To complete your registration, please visit the following link:\n" + tiny_url + "\n\n" + "If you are still having problems signing up please contact a member of our support staff at csdt.community@gmail.com\n\n" + "If you have received this message in error, or did not intend to register with the CSDT Community for any reason, please disregard this message entirely.\n\n" + "All the best,\n" + "- The CSDT Community"
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

    # Decrypts the ciphertext with ezPyCrypto's default algorithm
    def decryptUrlQuery(self, ciphertext):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.decryptUrlQuery()")

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

    # Creates new user with permissions set as public
    def createPublicAccount(self, first_name, last_name, username, password, email):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.createPublicAccount()")

        # Creates a user
        sql = "INSERT INTO users (first_name, last_name, email) VALUES ('%s', '%s', '%s');" % (str(first_name), str(last_name), str(email))
        user_id = database.executeInsertQuery(sql)
        log.debug("user_id = %s" % user_id)

        # Creates a username
        sql = "INSERT INTO usernames (user_id, username, pass) VALUES (\'%s\', \'%s\', \'%s\');" % (str(user_id), str(username), str(password))
        result = database.executeInsertQuery(sql)

        # Creates a user profile entry
        sql = "INSERT INTO user_profile (user_id, about) VALUES (\'%s\', \'%s\');" % (str(user_id), '')
        result = database.executeInsertQuery(sql)

        return user_id

    # Returns the username, first name, last name, email, and about me information of a user given their user_id
    def getUserProfileInformation(self, user_id):
        log = logging.getLogger('csdt')
        log.info("RegisterPublic.getUserProfileInformation()")
    
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


