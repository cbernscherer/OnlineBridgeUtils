# tournadmin
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField, BooleanField
from wtforms.fields.html5 import IntegerField, URLField, DateTimeField
from wtforms.validators import ValidationError, NumberRange, InputRequired, Length
from flask_user import current_user
from OnlineBridge.users.models import Role

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


class NewTournamentForm(FlaskForm):
    name = StringField('Bezeichnung', validators=[InputRequired(), Length(message='Maximal 50 Zeichen', max=50)],
                       render_kw={'autofocus': True})
    tournament_type = RadioField('Turniertyp', choices=[('P', 'Paar'), ('T', 'Team')], default='P')
    assistant_td = SelectField('zweiter TL', coerce=int)
    nr_of_sessions = IntegerField('Anzahl Sessions', default=1, validators=[
        InputRequired(), NumberRange(message='zwischen 1 und 10', min=1, max=10)
    ])

    info = URLField('Weitere Informationen unter', validators=[Length(message='Maximal 128 Zeichen', max=128)])
    use_profile_name = BooleanField('Namen aus dem Userprofile verwenden', default='checked')
    last_name_first = BooleanField('Familiennamen zuerst in pers Links')
    last_name_cap = BooleanField('Familiennamen in Blockschrift')

    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(NewTournamentForm, self).__init__(*args, **kwargs)

        role = Role.query.filter_by(name='Director').first_or_404()

        self.assistant_td.choices = []
        for user in role.users:
            if user.id != current_user.id:
                self.assistant_td.choices.append((user.id, user.member.alias_list_name))

        if len(self.assistant_td.choices) > 0:
            self.assistant_td.choices.sort(lambda x: x[1])