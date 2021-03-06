from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from OnlineBridge.config import ConfigApp
import os

basedir = os.path.abspath(os.path.dirname(__file__))
CONV_CARD_FOLDER = os.path.join(basedir, 'static', 'conv_cards')

# for federation members file upload
MEMBER_FILENAME = 'SpoXls.xls'
MEMBER_MAPPING = {
    'fed_nr': 'NR',
    'first_name': 'VNAME',
    'last_name': 'NAME'
}

app = Flask(__name__)
app.config.from_object(ConfigApp())

db = SQLAlchemy(app)

from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_babelex import Babel

Bootstrap(app)

from OnlineBridge.users.models import User, Role, UserRoles, Member
from OnlineBridge.conv_cards.models import playercards, ConvCard
from OnlineBridge.tournadmin.models import VPScale, TimeDisplay, ScoringMethod

Migrate(app, db)

mail = Mail(app)
babel = Babel(app)

from OnlineBridge.users.user_manager import MyUserManager
user_manager = MyUserManager(app, db, User)

from utilities.populate_db import populate
try:
    populate()
except:
    # error if the database has not been set up yet
    pass

from OnlineBridge.error_pages.handlers import error_pages
from OnlineBridge.core.views import core
from OnlineBridge.admin.views import admin
from OnlineBridge.conv_cards.views import conv_cards
from OnlineBridge.tournadmin.views import tournadmin

app.register_blueprint(error_pages)
app.register_blueprint(core)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(conv_cards, url_prefix='/conv_cards')
app.register_blueprint(tournadmin, url_prefix='/tournaments/admin')