from flask_wtf import FlaskForm
from wtforms.fields import FileField, SubmitField, StringField, BooleanField, SelectField
from wtforms.widgets import CheckboxInput
from wtforms.validators import InputRequired, ValidationError, Length, Regexp
from OnlineBridge import MEMBER_FILENAME

class PlayerUploadForm(FlaskForm):
    player_file = FileField(u'ÖBV Datei', description=MEMBER_FILENAME, validators=[InputRequired()],
                            render_kw={'autofocus':True, 'accept': '.xls, .xlsx'})
    submit = SubmitField(u'Hochladen')

    def validate_player_file(self, field):
        if not self.player_file.data:
            raise ValidationError('keine Datei ausgewählt')

        if self.player_file.data.filename != MEMBER_FILENAME:
            raise ValidationError(f'falsche Datei: es sollte {MEMBER_FILENAME} sein.')


class GuestDetailForm(FlaskForm):
    country_code = StringField('Staat')
    first_name = StringField('Vorname', validators=[InputRequired(), Length(max=50)])
    last_name = StringField('Familienname', validators=[InputRequired(), Length(max=50)])
    submit = SubmitField('Speichern')

    def __init__(self, new_guest:bool, *args, **kwargs):
        super(GuestDetailForm, self).__init__(*args, **kwargs)

        if new_guest:
            self.country_code.validators = [InputRequired(), Regexp('^[A-Za-z]{3}$', message='Falsche Form (XXX)')]
            self.country_code.render_kw = {
                'autofocus': True,
                'list': 'ctry_codes_list',
                'placeholder ': 'XXX'
            }
        else:
            self.first_name.render_kw = {
                'autofocus': True
            }


class UserDetailForm(FlaskForm):
    privileges = SelectField('Berechtigungen', coerce=int, render_kw={'autofocus': True}, choices= [
        (1, 'Player'), (2, 'Director'), (3, 'Admin'), (4, 'Superuser')
    ])
    active = BooleanField('aktiv', widget=CheckboxInput())
    submit = SubmitField('Speichern')


class CountryForm(FlaskForm):
    code = StringField('Code', validators=[Regexp(regex='^[a-zA-Z]{3}$', message='Falsche Form XXX'),
                                                            InputRequired()],
                       render_kw={'autofocus': True, 'placeholder': "XXX"},
                       filters=[lambda x: x.upper()])
    name = StringField('Name', validators=[InputRequired(), Length(max=50, message='maximal 50 Zeichen')])
    submit = SubmitField('Speichern')