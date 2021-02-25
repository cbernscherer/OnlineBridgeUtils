from flask import Blueprint, request, render_template, redirect, url_for, flash
from OnlineBridge import db
from flask_user import current_user, login_required, roles_required
from OnlineBridge.users.models import Member
from OnlineBridge.conv_cards.models import ConvCard
from OnlineBridge.conv_cards.forms import NewCardForm

conv_cards = Blueprint('conv_cards', __name__, template_folder='templates/conv_cards')

@conv_cards.route('/new_card', methods=['GET', 'POST'])
def new_card():
    form = NewCardForm()

    # get all the players with whom the current user has already cards stored

    if request.method == "POST" and form.validate_on_submit():
        pass