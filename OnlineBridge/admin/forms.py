from flask_wtf import FlaskForm
from wtforms.fields import FileField, SubmitField, StringField
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
            self.country_code.validators = [InputRequired(), Regexp('^[A-Z]{3}$', message='Falsche Form (XXX)')]
            self.country_code.render_kw = {
                'autofocus': True,
                'list': 'ctry_codes_list',
                'placeholder ': 'XXX'
            }
        else:
            self.first_name.render_kw = {
                'autofocus': True
            }