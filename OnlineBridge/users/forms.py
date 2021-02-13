from wtforms import StringField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, Regexp

# Customize the Register form:
from flask_user.forms import RegisterForm
class MyRegisterForm(RegisterForm):
    # Add fields for member validation
    oebv_nr = IntegerField('ÖBV-Nummer')
    guest_nr = StringField('Gast ID', validators=[
        Length(max=7),
        Regexp(regex=r'^[A-Z{3}[0-9]{4}$', message='Falsche Form')
    ])
    last_name = StringField('Familienname', validators=[
        InputRequired(), Length(max=50)
    ])