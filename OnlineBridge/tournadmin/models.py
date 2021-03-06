# tournadmin
from OnlineBridge import db


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