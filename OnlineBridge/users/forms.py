from wtforms import StringField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, Regexp

# Customize the Register form:
from flask_user.forms import RegisterForm, LoginForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password.label.text = 'Passwort'
        self.retype_password.label.text = 'Passwort bestätigen'
        self.submit.label.text = 'Registrieren'
        self.guest_nr.description = 'Form XXX9999'

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.password.label.text = 'Passwort'
        self.remember_me.label.text = 'angemeldet bleiben'
        self.submit.label.text = 'Anmelden'