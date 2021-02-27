import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from OnlineBridge import db, CONV_CARD_FOLDER
from flask_user import current_user, login_required, roles_required
from OnlineBridge.users.models import Member
from OnlineBridge.conv_cards.models import ConvCard
from OnlineBridge.conv_cards.forms import NewCardForm, SearchPlayerForm, ConfDeleteForm
from math import ceil

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
                file.save(os.path.join(CONV_CARD_FOLDER, conv_card.filename))

                return redirect(url_for('conv_cards.list_cards'))

    possible_partners = Member.query.filter(Member.id.notin_(exclude_ids)).\
        order_by(Member.last_name.asc(), Member.first_name.asc()).all()

    context = {
        'form': form,
        'possible_partners': possible_partners
    }

    return render_template('new_card.html', **context)


@conv_cards.route('/list_cards')
@login_required
def list_cards():
    per_page = 12

    # get arguments
    page = request.args.get('page', 1, type=int)
    slug = request.args.get('slug', '', type=str)

    own_cards = True

    # retrieve player
    if slug == '':
        member = current_user.member
    else:
        if not current_user.has_roles('Director'):
            abort(403)
        own_cards = False
        member = Member.query.filter_by(slug=slug).first_or_404()

    # retrieve partners
    partners = []
    for card in member.my_cards:
        for player in card.players:
            if player.id != member.id:
                partners.append({'list_name': player.list_name, 'card': card})

    partners.sort(key=lambda p:p['list_name'])

    # prepare pagination
    num_pages = ceil(len(partners) / per_page)
    page = min(page, num_pages)
    page = max(page, 1)
    if len(partners) > 0:
        partners = partners[(page-1)*per_page:page*per_page]

    pages = range(1, num_pages+1)

    context = {
        'pages': pages,
        'page': page,
        'partners': partners,
        'player': member,
        'own_cards': own_cards,
        'num_pages': num_pages,
        'slug': slug
    }
    return render_template('list_cards.html', **context)


@conv_cards.route('/search_player', methods=['GET', 'POST'])
@roles_required('Director')
def search_player():
    if ConvCard.query.count() == 0:
        flash('Noch keine Konventionskarten vorhanden', category='info')
        return redirect(url_for('core.index'))

    form = SearchPlayerForm()
    if request.method == "POST" and form.validate_on_submit():
        return redirect(url_for('conv_cards.list_cards', slug=form.player_found.slug))

    # get players with convention cards
    players = []
    for card in ConvCard.query.all():
        for player in card.players:
            players.append(player.id)

    players = set(players)

    card_players = Member.query.filter(Member.id.in_(players)).\
        order_by(Member.last_name.asc(), Member.first_name.asc()).all()

    context = {
        'form': form,
        'players': card_players
    }
    return render_template('search_player.html', **context)


@conv_cards.route('/<string:slug>/<pl_slug>/conf_delete', methods=['GET', 'POST'])
@roles_required('Superuser')
def conf_delete(slug, pl_slug):
    card = ConvCard.query.filter_by(slug=slug).first_or_404()

    form = ConfDeleteForm()

    if request.method == "POST" and form.validate_on_submit():
        filename = card.filename

        db.session.delete(card)
        db.session.commit()

        os.remove(os.path.join(CONV_CARD_FOLDER, filename))

        flash('Karte gelöscht', 'succes')
        return redirect(url_for('conv_cards.list_cards', slug=pl_slug))

    return render_template('conf_delete.html', form=form, card=card, pl_slug=pl_slug)