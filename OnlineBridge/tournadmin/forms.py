# tournadmin
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import ValidationError, NumberRange, InputRequired, Length

class ParameterForm(FlaskForm):
    id = IntegerField('Schlüssel')

    name = StringField('Bezeichnung', validators=[InputRequired(), Length(message='Maximal 64 Zeichen', max=64)])
    tournament_type = RadioField('Turniertyp', choices=[('P', 'Paar'), ('T', 'Team')], default='T')
    submit = SubmitField('Speichern')

    def __init__(self, new_param:bool, model, param_id, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.new_param = new_param
        self.model = model
        self.param_id = param_id

        if self.new_param:
            self.id.render_kw = {'autofocus': True}
            self.id.validators = [
                InputRequired(),
                NumberRange(message='Nur Werte zwischen 0 und 100', min=0, max=100)]
        else:
            self.id.render_kw = {'disabled': True}
            self.name.render_kw = {'autofocus': True}

    def validate_id(self, field):

        if self.new_param:
            parameter = self.model.query.filter_by(id=self.id.data).one_or_none()
            if parameter:
                raise ValidationError('Dieser Schlüssel existiert schon')

    def validate_name(self, field):
        comp_id = self.param_id
        if self.id.data:
            comp_id = self.id.data

        parameter = self.model.query.filter(self.model.id.__ne__(comp_id)).\
            filter_by(name=self.name.data).one_or_none()

        if parameter:
            raise ValidationError('Diese Bezeichnung existiert schon')