from flask_wtf import FlaskForm
from wtforms.fields import FileField, SubmitField
from wtforms.validators import InputRequired, ValidationError
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