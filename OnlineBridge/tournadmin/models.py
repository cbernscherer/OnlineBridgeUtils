# tournadmin
from OnlineBridge import db
from utilities import create_random_slug
from datetime import datetime


class VPScale(db.Model):

    __tablename__ = 'vpscales'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class TimeDisplay(db.Model):

    __tablename__ = 'timedisplays'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class ScoringMethod(db.Model):

    __tablename__ = 'scoringmethods'

    id = db.Column(db.Integer(), primary_key=True)
    tournament_type = db.Column(db.String(1), default='T', nullable=False)  # P(airs) T(eams)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Tournament(db.Model):

    __tablename__ = 'tournaments'

    id = db.Column(db.BigInteger(), primary_key=True)
    slug = db.Column(db.String(24), nullable=False, index=True, default=create_random_slug(24))

    name = db.Column(db.String(50), nullable=False)
    tournament_type = db.Column(db.String(1), nullable=False, default='P') # P Pairs T Teams
    info = db.Column(db.String(128)) # URL
    status = db.Column(db.SmallInteger(), nullable=False, default=1) # 1 created 2 registration 3 running 4 closed

    # parameters how player names will be shown
    use_profile_name = db.Column(db.Boolean(), default=True, nullable=False)
    last_name_first = db.Column(db.Boolean(), default=False, nullable=False)
    last_name_cap = db.Column(db.Boolean(), default=False, nullable=False)

    sessions = db.relationship('Session', backref='tournament', lazy='dynamic')

    director_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ass_director_id = db.Column(db.Integer(), index=True)


class Session(db.Model):

    __tablename__ = 'sessions'

    id = db.Column(db.BigInteger(), primary_key=True)

    starting_time = db.Column(db.DateTime(), nullable=False, default=datetime.today)
    session_nr = db.Column(db.SmallInteger(), nullable=False, default=1)

    baselink = db.Column(db.String(128)) # URL to RealBridge session
    config_file = db.Column(db.String(64))

    # RealBridge parameters
    name = db.Column(db.String(50))
    club_name = db.Column(db.String(50))
    club_id = db.Column(db.String(20))
    scoring_method = db.Column(db.SmallInteger())
    vp_scale = db.Column(db.SmallInteger())
    time_display = db.Column(db.SmallInteger())
    num_tables = db.Column(db.SmallInteger())
    num_roundsnum_rounds = db.Column(db.SmallInteger())
    boards_per_round = db.Column(db.SmallInteger())
    time_per_round = db.Column(db.Integer()) # seconds
    first_board = db.Column(db.SmallInteger(), default=1)
    use_screen = db.Column(db.Boolean(), default=False)
    written_explanation = db.Column(db.Boolean(), default=False)
    scoring_break = db.Column(db.Boolean(), default=False)
    prevent_unreserved_login = db.Column(db.Boolean(), default=False)
    # trick one delays
    opening_lead = db.Column(db.SmallInteger(), default=10)
    dummy = db.Column(db.SmallInteger(), default=0)
    third_hand = db.Column(db.SmallInteger(), default=0)

    tournament_id = db.Column(db.BigInteger(), db.ForeignKey(Tournament.id, ondelete='CASCADE'), nullable=False)
    tournament_session_unique = db.UniqueConstraint('tournament_id', 'session_nr')