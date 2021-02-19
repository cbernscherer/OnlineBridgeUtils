from flask_wtf import FlaskForm
from wtforms.fields import FileField, SubmitField
from wtforms.validators import InputRequired, ValidationError

class PlayerUploadForm(FlaskForm):
    player_file = FileField(u'ÖBV Datei', description='SpoXls.xls', validators=[InputRequired()],
                            render_kw={'autofocus':True, 'accept': '.xls, .xlsx'})
    submit = SubmitField(u'Hochladen')

    def validate_player_file(self, field):
        if not self.player_file.data:
            raise ValidationError('keine Datei ausgew&auml;hlt')

        fn = self.player_file.data.filename
        if not fn.split('.')[-1] in ['xls', 'xlsx']:
            raise ValidationError('keine Excel Datei')