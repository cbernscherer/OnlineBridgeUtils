# tournadmin
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField, RadioField
from wtforms.validators import ValidationError, NumberRange, InputRequired, Length
from wtforms.widgets import HiddenInput
from OnlineBridge.tournadmin.models import ScoringMethod

class ParameterForm(FlaskForm):
    id = IntegerField('Schlüssel', validators=[
        InputRequired(),
        NumberRange(message='Nur Werte zwischen 0 und 100', min=0, max=100)])

    name = StringField('Bezeichnung', validators=[InputRequired(), Length(message='Maximal 64 Zeichen', max=64)])
    tournament_type = RadioField('Turniertyp', choices=[('P', 'Paar'), ('T', 'Team')], default='T')
    submit = SubmitField('Speichern')

    def __init__(self, new_param:bool, model, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.new_param = new_param
        self.model = model

        if self.model != ScoringMethod:
            self.tournament_type.widget = HiddenInput()

        if self.new_param:
            self.id.render_kw = {'autofocus': True}
        else:
            self.id.render_kw = {'disabled': True}
            self.name.render_kw = {'autofocus': True}

    def validate_id(self, field):
        parameter = self.model.query.filter_by(id=self.id.data).one_or_none()

        if self.new_param and parameter:
            raise ValidationError('Diese ID existiert schon')

    def validate_name(self, field):
        parameter = self.model.query.filter_by(self.model.id.__ne__(self.id.data)).\
            filter_by(name=self.name.data).one_or_none()

        if parameter:
            raise ValidationError('Diese Bezeichnung existiert schon')