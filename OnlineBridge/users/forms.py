from wtforms import StringField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from utilities.my_validators import MyRegExValidator
from OnlineBridge.users.models import Member
from flask_user.forms import RegisterForm, LoginForm, ResendEmailConfirmationForm, ChangePasswordForm

# Customize the Register form:
class MyRegisterForm(RegisterForm):
    # Add fields for member validation
    oebv_nr = IntegerField('ÖBV-Nummer', default=0, validators=[InputRequired()])
    guest_nr = StringField('Gast ID', validators=[
        Length(max=7),
        MyRegExValidator(regex='^[A-Z]{3}[0-9]{4}$')
    ], render_kw={
        'placeholder': "XXX9999"
    })
    last_name = StringField('Familienname', validators=[
        InputRequired(), Length(max=50)
    ])

    def __init__(self, *args, **kwargs):
        super(MyRegisterForm, self).__init__(*args, **kwargs)

        self.password.label.text = 'Passwort'
        self.retype_password.label.text = 'Passwort bestätigen'
        self.submit.label.text = 'Registrieren'
        self.email.render_kw = {'autofocus': True}

    def validate_oebv_nr(self, oebv_nr):
        if (oebv_nr.data > 0) and self.guest_nr.data:
            raise ValidationError('Es darf nur entweder die ÖBV-Nr oder die Gast ID angegeben werden')

        if (oebv_nr.data <= 0) and not self.guest_nr.data:
            raise ValidationError('Bitte ÖBV-Nr oder Gast ID angeben')

    def validate_last_name(self, last_name):
        oebv_nr = self.oebv_nr.data
        guest_nr = self.guest_nr.data
        member = None

        not_valid_mess = 'Abgleich mit Spielertabelle fehlgeschlagen'
        already_exist_mess = 'Zu diesem Spieler gibt es schon einen Benutzer'

        if oebv_nr and oebv_nr > 0:
            member = Member.query.filter_by(fed_nr=oebv_nr).first()
        elif guest_nr:
            member = Member.query.filter_by(guest_nr=guest_nr).first()

        if not member:
            raise ValidationError(not_valid_mess)

        if member.user:
            raise ValidationError(already_exist_mess)

        if not (last_name.data and (last_name.data[:3].lower() == member.last_name[:3].lower())):
            raise ValidationError(not_valid_mess)


class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)

        self.password.label.text = 'Passwort'
        self.remember_me.label.text = 'angemeldet bleiben'
        self.submit.label.text = 'Anmelden'
        self.email.render_kw = {'autofocus': True}


class MyResendEmailConfirmationForm(ResendEmailConfirmationForm):

    def __init__(self, *args, **kwargs):
        super(MyResendEmailConfirmationForm, self).__init__(*args, **kwargs)

        self.email.render_kw = {'autofocus': True}
        self.email.label.text = 'Deine Email'
        self.submit.label.text = 'Erneut senden'


class MyChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyChangePasswordForm, self).__init__(*args, **kwargs)

        self.old_password.render_kw = {'autofocus': True}
        self.old_password.label.text = 'Altes Passwort'
        self.new_password.label.text = 'Neues Passwort'
        self.retype_password.label.text = 'Passwort bestätigen'
        self.submit.label.text = 'Passwort ändern'