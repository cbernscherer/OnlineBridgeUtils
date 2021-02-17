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
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = False

class ConfigAuth:
    USER_ENABLE_CONFIRM_EMAIL = True
    USER_ENABLE_USERNAME = False
    USER_ENABLE_CHANGE_USERNAME = False
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False

    USER_AUTO_LOGIN_AFTER_REGISTER = False
    USER_APP_NAME = 'Online Bridge Utilities'
    USER_EMAIL_SENDER_EMAIL = os.environ['EMAIL_USER']
    USER_SEND_REGISTERED_EMAIL = True
    USER_SEND_USERNAME_CHANGED_EMAIL = False
    USER_SHOW_EMAIL_DOES_NOT_EXIST = True

    USER_AFTER_REGISTER_ENDPOINT = 'core.reg_complete'
    USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT  = 'core.reg_complete'
    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = 'user.login'


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