from OnlineBridge import db
from utilities.sluggenerator import create_random_slug
from datetime import datetime


playercards = db.table(
    'playercards',
    db.Column('member_id', db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), primary_key=True),
    db.Column('convcards_id', db.Integer, db.ForeignKey('convcards.id', ondelete='CASCADE'), primary_key=True)
)


class ConvCard(db.Model):

    __tablename__ = 'convcards'

    id = db.Column(db.Integer(), primary_key=True)
    slug = db.Column(db.String(24), unique=True, nullable=False, index=True, default=create_random_slug(24))
    uploaded = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    # reference to members
    players = db.relationship('Member', secondary=playercards, lazy='subquery', back_populates='my_cards')

    @property
    def filename(self):
        return f'cc{self.slug}.pdf'

    def __commit_delete__(self):
        # delete the file
        pass