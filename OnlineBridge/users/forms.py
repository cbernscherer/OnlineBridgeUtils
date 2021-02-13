from wtforms import StringField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length

# Customize the Register form:
from flask_user.forms import RegisterForm
class MyRegisterForm(RegisterForm):
    # Add fields for member validation
    oebv_nr = IntegerField('ÖBV-Nummer')
    guest_nr = StringField('Gast ID', validators=[
        Length(max=10)
    ])
    last_name = StringField('Familienname', validators=[
        InputRequired(), Length(max=50)
    ])