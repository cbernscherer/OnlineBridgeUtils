from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_user import roles_required, current_user
from OnlineBridge.admin.forms import PlayerUploadForm, GuestDetailForm, UserDetailForm
from OnlineBridge.users.models import Member, User, Role
from OnlineBridge import db
from utilities.populate_db import fed_members_upload
from math import ceil

admin = Blueprint('admin', __name__, template_folder='templates/admin')

roles_as_str = ['Player', 'Director', 'Admin', 'Superuser']

@admin.route('/player_upload', methods=['GET', 'POST'])
@roles_required('Admin')
def player_upload():
    form = PlayerUploadForm()

    if request.method == 'POST' and form.validate_on_submit():
        success = False

        if 'player_file' in request.files:
            try:
                success = fed_members_upload(request.files['player_file'])
            except:
                pass

        if success:
            flash(u'Upload abgeschlossen', 'success')
        else:
            flash(u'Upload fehlgeschlagen', 'error')

        return redirect(url_for('core.index'))

    return render_template('oebv_players_upload.html', form=form)


@admin.route('/guests')
@roles_required('Admin')
def guests_page():
    per_page = 15
    page = request.args.get('page', 1, type=int)

    last_page = ceil(Member.query.filter(Member.guest_nr.isnot(None)).count() / per_page)

    page = min(page, last_page)
    page = max(page, 1)

    # Grab a list of guests from database.
    guests = Member.query.filter(Member.guest_nr.isnot(None)).\
        order_by(Member.last_name.asc()).paginate(page=page, per_page=per_page)
    return render_template('guests.html', guests=guests)


@admin.route('/guest/<slug>/update', methods=['GET', 'POST'])
@roles_required('Admin')
def guest_update(slug):
    form = GuestDetailForm(False)
    guest = Member.query.filter_by(slug=slug).one_or_none()
    if not guest:
        abort(404)

    if request.method == "POST" and form.validate_on_submit():
        guest.first_name = form.first_name.data.title()
        guest.last_name = form.last_name.data.title()

        db.session.add(guest)
        db.session.commit()

        return redirect(url_for('admin.guests_page'))

    elif request.method == 'GET':
        form.first_name.data = guest.first_name
        form.last_name.data = guest.last_name

    context = {
        'form': form,
        'new_guest': False,
        'guest': guest
    }

    return render_template('guest_detail.html', **context)


@admin.route('/guest/new', methods=['GET', 'POST'])
@roles_required('Admin')
def guest_new():
    form = GuestDetailForm(True)

    if request.method == "POST" and form.validate_on_submit():
        # get the next available number for a country
        next_nr = 1
        guests = Member.query.filter(Member.guest_nr.startswith(form.country_code.data)).all()

        if len(guests) > 0:
            nrs = [int(g.guest_nr[3:]) for g in guests]
            next_nr = max(nrs) + 1

        guest = Member(
            guest_nr=form.country_code.data + '{:04d}'.format(next_nr),
            first_name=form.first_name.data.title(),
            last_name=form.last_name.data.title()
        )

        db.session.add(guest)
        db.session.commit()

        return redirect(url_for('admin.guests_page'))

    # create datalist for choices
    ctry_codes = []
    guests = Member.query.filter(Member.guest_nr.isnot(None)).all()

    if len(guests) > 0:
        ctry_codes = list(set([g.guest_nr[:3] for g in guests]))
        ctry_codes.sort()

    context = {
        'form': form,
        'new_guest': True,
        'ctry_codes': ctry_codes
    }

    return render_template('guest_detail.html', **context)


@admin.route('/guest/<slug>/delete', methods=['GET'])
@roles_required('Admin')
def guest_delete(slug):

    guest = Member.query.filter_by(slug=slug).one_or_none()
    if not guest:
        abort(404)

    if request.method == "GET":

        db.session.delete(guest)
        db.session.commit()

    return redirect(url_for('admin.guests_page'))


@admin.route('/registered_users')
@roles_required('Superuser')
def registered_users():
    per_page = 15
    page = request.args.get('page', 1, type=int)

    last_page = ceil(User.query.filter(User.id.__ne__(current_user.id)).count() / per_page)

    page = min(page, last_page)
    page = max(page, 1)

    reg_users = User.query.filter(User.id.__ne__(current_user.id)).\
        order_by(User.last_name.asc(), User.first_name.asc()).paginate(page=page, per_page=per_page)

    context = {
        'reg_users': reg_users,
        'roles_as_str': roles_as_str
    }

    return render_template('reg_users_list.html', **context)


@admin.route('/user_detail/<string:slug>/<int:page>', methods=['GET', 'POST'])
@roles_required('Superuser')
def user_detail(slug, page):
    user = User.query.filter_by(slug=slug).first_or_404()

    form = UserDetailForm()

    if request.method == "POST" and form.validate_on_submit():

        roles = []
        for r in roles_as_str:
            roles.append(Role.query.filter_by(name=r).one())

        user.roles = roles[:form.privileges.data]
        user.active = form.active.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.registered_users', page=page))

    elif request.method == 'GET':
        form.privileges.data = len(user.roles)
        print(len(user.roles))
        form.active.data = user.active

    context = {
        'user': user,
        'form': form,
        'page': page
    }

    return render_template('user_detail.html', **context)