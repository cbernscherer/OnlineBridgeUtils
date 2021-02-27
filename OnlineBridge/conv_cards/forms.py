from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from OnlineBridge.users.models import Member


class NewCardForm(FlaskForm):
    partner = StringField('Partner', validators=[InputRequired(), Length(max=128)], render_kw={
        'autofocus': True, 'list': 'memberlist'
    })

    conv_card = FileField('Konventionskarte (PDF), maximal 2MB', validators=[InputRequired()],
                          render_kw={'accept': '.pdf'})
    submit = SubmitField('Hochladen')

    def __init__(self, *args, **kwargs):
        super(NewCardForm, self).__init__(*args, **kwargs)
        self.partner_found = None

    def validate_conv_card(self, field):
        if not self.conv_card.data:
            raise ValidationError('keine Datei ausgewählt')

        if (len(self.conv_card.data.filename) < 5) or (self.conv_card.data.filename[-4:].lower() != '.pdf'):
            raise ValidationError(f'Keine PDF-Datei')

    def validate_partner(self, field):
        if len(self.partner.data) == 0:
            raise ValidationError('kein Partner angegeben')

        partner_nr = str(self.partner.data).split()[-1]
        self.partner_found = None

        if partner_nr.isdigit():
            self.partner_found = Member.query.filter_by(fed_nr=int(partner_nr)).one_or_none()
        else:
            self.partner_found = Member.query.filter_by(guest_nr=partner_nr).one_or_none()

        if self.partner_found is None:
            raise ValidationError('der Partner konnte nicht gefunden werden')


class SearchPlayerForm(FlaskForm):
    player = StringField('Spieler', validators=[InputRequired(), Length(max=128)], render_kw={
        'autofocus': True, 'list': 'memberlist'
    })
    submit = SubmitField('Suchen')

    def __init__(self, *args, **kwargs):
        super(SearchPlayerForm, self).__init__(*args, **kwargs)
        self.player_found = None

    def validate_player(self, field):
        if len(self.player.data) == 0:
            raise ValidationError('kein Spieler angegeben')

        player_nr = str(self.player.data).split()[-1]
        self.player_found = None

        if player_nr.isdigit():
            self.player_found = Member.query.filter_by(fed_nr=int(player_nr)).one_or_none()
        else:
            self.player_found = Member.query.filter_by(guest_nr=player_nr).one_or_none()

        if self.player_found is None:
            raise ValidationError('der Spieler konnte nicht gefunden werden')