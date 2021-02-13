from OnlineBridge import db
from flask_user import UserMixin
from utilities import create_random_slug

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False)

    # User fields
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(1), nullable=False, default='f') # f female m male

    slug = db.Column(db.String(24), nullable=False, unique=True, index=True, default=create_random_slug(24))

    # Relationships
    roles = db.relationship('Role', secondary='user_roles')

    # federation members
    member_id = db.Column(db.Integer(), db.ForeignKey('members.id', ondelete='CASCADE'))



# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# federation members
class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer(), primary_key=True)
    slug = db.Column(db.String(24), nullable=False, index=True, unique=True, default=create_random_slug(24))

    # federation member number
    fed_nr = db.Column(db.Integer(), nullable=True, unique=True, index=True)
    guest_nr = db.Column(db.String(10), nullable=True, unique=True, index=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref='member', uselist=False)