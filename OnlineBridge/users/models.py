from OnlineBridge import db
from flask_user import UserMixin
from utilities import create_random_slug
from OnlineBridge.conv_cards.models import playercards

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False)

    # User fields
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(50), nullable=False, default='MISSING')
    last_name = db.Column(db.String(50), nullable=False, default='MISSING')
    sex = db.Column(db.String(1), nullable=False, default='f') # f female m male

    slug = db.Column(db.String(24), nullable=False, unique=True, index=True, default=create_random_slug(24))

    # Relationships
    roles = db.relationship('Role', secondary='user_roles', backref='users', lazy=True)
    director_of = db.relationship('Tournament', backref='director', lazy='dynamic')

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

    user = db.relationship('User', backref='member', uselist=False, cascade="all, delete-orphan")

    # reference to convcards
    my_cards = db.relationship('ConvCard', secondary=playercards, lazy='subquery', back_populates='players')

    @property
    def list_name(self):
        return ' '.join([self.last_name, self.first_name])

    @property
    def alias_list_name(self):
        if not self.user:
            return None

        alias = ' '.join([self.user.last_name, self.user.first_name])

        if alias == self.list_name:
            return None

        return alias

    def __repr__(self):
        if self.fed_nr:
            return f'{self.fed_nr} {self.last_name} {self.first_name}'
        else:
            return f'{self.guest_nr} {self.last_name} {self.first_name}'