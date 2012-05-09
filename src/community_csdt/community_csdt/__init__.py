from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings

import ezPyCrypto
import logging
import os

# Sets up symmetric encryption key for encryption of url query strings. 
# Key size is 1024 bits. Default encryption algorithm is blowfish.
def setupKey():
    key = ezPyCrypto.key(1024)
    public_key = key.exportKey()
    private_key = key.exportKeyPrivate()
    
    # Path = ../email_key.pub
    path = os.path.join(os.path.dirname(__file__), '..', 'email_key.pub')
    fd = open(path, "w")
    fd.write(public_key)
    fd.close()

    # Path = ../email_key.priv
    path = os.path.join(os.path.dirname(__file__), '..', 'email_key.priv')
    fd = open(path, "w")
    fd.write(private_key)
    fd.close()

    return

# Sets up the logger
def setupLogger():
    # Path = log/csdt.log
    path = os.path.join(os.path.dirname(__file__), 'log', 'csdt.log') 
    LOG_FILENAME = path

    # Set up a specific logger with our desired output level
    logger = logging.getLogger('csdt')
    logger.setLevel(logging.DEBUG)
    #logger.setLevel(logging.ERROR)

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=5)

    # Prints timestamp next to each logged message
    formatter = logging.Formatter('%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return

def main(global_config, **settings):
    setupLogger()
    setupKey()

    """ This function returns a Pyramid WSGI application."""
    session_factory = session_factory_from_settings(settings)

    config = Configurator(settings=settings, root_factory='community_csdt.src.models.root.Root')
    config.set_session_factory(session_factory)

    config.add_static_view(name='log', path='community_csdt:log')
    config.add_static_view(name='static', path='community_csdt:static')
    config.add_static_view(name='uploads', path='community_csdt:uploads')

    config.scan()
    return config.make_wsgi_app()


