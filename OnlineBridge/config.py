import os
from utilities import create_random_slug

basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigMail:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = 'Christian Bernscherer'

class ConfigAuth:
    USER_ENABLE_USERNAME = False
    USER_ENABLE_CHANGE_USERNAME = False

    USER_AUTO_LOGIN_AFTER_REGISTER = False
    USER_APP_NAME = 'Online Bridge Utilities'
    USER_EMAIL_SENDER_EMAIL = os.environ['EMAIL_USER']
    USER_SEND_REGISTERED_EMAIL = False
    USER_SEND_USERNAME_CHANGED_EMAIL = False
    USER_SHOW_EMAIL_DOES_NOT_EXIST = True


class ConfigApp(ConfigMail, ConfigAuth):

    TESTING = True

    # Key for Forms
    @property
    def SECRET_KEY(self):
        if  not 'FLASK_SECRET_KEY' in os.environ:
            os.environ['FLASK_SECRET_KEY'] = create_random_slug(64)()
        return os.environ['FLASK_SECRET_KEY']

    ############################################

            # SQL DATABASE

    ##########################################

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    SQLALCHEMY_TRACK_MODIFICATIONS = False