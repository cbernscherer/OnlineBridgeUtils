from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from OnlineBridge.users.user_manager import MyUserManager
from OnlineBridge.config import ConfigApp

app = Flask(__name__)
app.config.from_object(ConfigApp())

db = SQLAlchemy(app)

from OnlineBridge.users.models import User, Role, UserRoles

Migrate(app, db)

user_manager = MyUserManager(app, db, User)

from utilities.populate_db import populate
try:
    populate()
except:
    # error if the database has not been set up yet
    pass

mail = Mail(app)

from OnlineBridge.error_pages.handlers import error_pages
from OnlineBridge.core.views import core

app.register_blueprint(error_pages)
app.register_blueprint(core)