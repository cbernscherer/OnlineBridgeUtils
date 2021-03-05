# tournadmin

from OnlineBridge import db


class ParameterType(db.Model):

    __tablename__ = 'parametertypes'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    parameters = db.relationship('Parameter', backref='parameter_type', lazy=True)

    def __repr__(self):
        return self.name


class Parameter(db.Model):

    __tablename__ = 'parameters'

    id = db.Column(db.Integer(), primary_key=True)
    parameter_type_id = db.Column(db.Integer() ,db.ForeignKey(ParameterType.id, ondelete='CASCADE'))

    value = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    unique_type_value = db.UniqueConstraint('parameter_type_id', 'value')
    unique_type_name = db.UniqueConstraint('parameter_type_id', 'name')

    def __repr__(self):
        return self.name