from os import path
from flask import Blueprint, request, render_template, redirect, url_for, flash
from OnlineBridge import db, CONV_CARD_FOLDER
from flask_user import current_user, login_required, roles_required
from OnlineBridge.users.models import Member
from OnlineBridge.conv_cards.models import ConvCard
from OnlineBridge.conv_cards.forms import NewCardForm

conv_cards = Blueprint('conv_cards', __name__, template_folder='templates/conv_cards')

@conv_cards.route('/new_card', methods=['GET', 'POST'])
@login_required
def new_card():
    form = NewCardForm()

    # get all the players with whom the current user has already cards stored
    exclude_ids = [current_user.member.id]
    for card in current_user.member.my_cards:
        for player in card.players:
            exclude_ids.append(player.id)
    exclude_ids = set(exclude_ids)

    if request.method == "POST" and form.validate_on_submit():
        if form.partner_found:
            if form.partner_found.id in exclude_ids:
                flash('Mit diesem Partner hast du schon eine Konventionskarte abgelegt', 'error')

            elif 'conv_card' not in request.files:
                flash('Fileanhang fehlt', 'error')

            else:
                file = request.files['conv_card']

                # new convention card
                conv_card = ConvCard()
                conv_card.players.append(current_user.member)
                conv_card.players.append(form.partner_found)

                # save to database
                db.session.add(conv_card)
                db.session.commit()

                # save file
                file.save(path.join(CONV_CARD_FOLDER, conv_card.filename))

                return redirect(url_for('core.index'))

    possible_partners = Member.query.filter(Member.id.notin_(exclude_ids)).\
        order_by(Member.last_name.asc(), Member.first_name.asc()).all()

    context = {
        'form': form,
        'possible_partners': possible_partners
    }

    return render_template('new_card.html', **context)