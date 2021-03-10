# tournadmin
from flask import Blueprint,request, render_template, redirect, abort, flash, url_for
from flask_user import login_required, roles_required, current_user
from OnlineBridge import db
from OnlineBridge.tournadmin.models import VPScale, ScoringMethod, TimeDisplay
from OnlineBridge.tournadmin.forms import ParameterForm
from utilities import pagination_setup

tournadmin = Blueprint('tournadmin', __name__, template_folder='templates/tournadmin')


@tournadmin.route('/vpscale/new', methods=['GET', 'POST'])
@roles_required('Superuser')
def new_vpscale():
    per_page = 10
    page, last_page = pagination_setup(per_page, VPScale)

    form = ParameterForm(True, VPScale, -1)

    if request.method == "POST" and form.validate_on_submit():
        vp_scale = VPScale(id=form.id.data, name=form.name.data)
        db.session.add(vp_scale)
        db.session.commit()

        return redirect(url_for('tournadmin.new_vpscale', page=page))

    vp_scales = VPScale.query.order_by(VPScale.id.asc()).paginate(page=page, per_page=per_page)

    context = {
        'form': form,
        'parameters': vp_scales,
        'show_tourn_type': False,
        'new_param': True,
        'param_type': ('VP Skala', 'VP Skalen', 'vp_scale')
    }
    return render_template('parameter.html', **context)


@tournadmin.route('/vpscale/<int:id>/update', methods=['GET', 'POST'])
@roles_required('Superuser')
def update_vpscale(id):
    per_page = 10
    page, last_page = pagination_setup(per_page, VPScale)

    vp_scale = VPScale.query.filter_by(id=id).first_or_404()

    form = ParameterForm(False, VPScale, vp_scale.id)

    if request.method == "POST" and form.validate_on_submit():
        vp_scale.name = form.name.data
        db.session.add(vp_scale)
        db.session.commit()

        return redirect(url_for('tournadmin.new_vpscale', page=page))

    elif request.method == 'GET':
        form.name.data = vp_scale.name

    form.id.data = vp_scale.id
    vp_scales = VPScale.query.order_by(VPScale.id.asc()).paginate(page=page, per_page=per_page)

    context = {
        'form': form,
        'parameters': vp_scales,
        'this_param': vp_scale,
        'show_tourn_type': False,
        'new_param': False,
        'param_type': ('VP Skala', 'VP Skalen', 'vp_scale')
    }
    return render_template('parameter.html', **context)