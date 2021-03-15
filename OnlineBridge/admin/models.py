from OnlineBridge import db
from utilities import create_random_slug

class Country(db.Model):

    __tablename__ = 'countries'

    id = db.Column(db.Integer(), primary_key=True)

    code = db.Column(db.String(3), nullable=False, unique=True, index=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # for fed_nr other than Austrian
    fed_nr_offset = db.Column(db.Integer(), nullable=True, unique=True)

    clubs = db.relationship('Club', backref='country', lazy=True)

    def __repr__(self):
        return f'{self.code} {self.name}'


class Club(db.Model):

    __tablename__ = 'clubs'

    id = db.Column(db.Integer(), primary_key=True)
    slug = db.Column(db.String(24), nullable=False, index=True, default=create_random_slug(24))

    country_id = db.Column(db.Integer(), db.ForeignKey(Country.id, ondelete='CASCADE'))

    club_nr = db.Column(db.Integer(), nullable=False)
    short = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    country_club_unique = db.UniqueConstraint('country_id', 'club_nr')
    country_clubshort_unique = db.UniqueConstraint('country_id', 'short')

    tournaments = db.relationship('Tournament', backref='club', lazy='dynamic')