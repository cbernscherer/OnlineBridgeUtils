# tournadmin
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import ValidationError, NumberRange, InputRequired, Length
from wtforms.widgets import HiddenInput
from OnlineBridge.tournadmin.models import ScoringMethod

class ParameterForm(FlaskForm):
    id = IntegerField('Schlüssel', validators=[InputRequired(), NumberRange(min=1, max=100)],
                      render_kw={'autofocus': True})
    name = StringField('Bezeichnung', validators=[InputRequired(), Length(max=64)])
    tournament_type = SelectField('Torniertyp', choices=[('P', 'Paar'), ('T', 'Team')], default='T')
    submit = SubmitField('Speichern')

    def __init__(self, model, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.model = model

        if self.model != ScoringMethod:
            self.tournament_type.widget = HiddenInput()