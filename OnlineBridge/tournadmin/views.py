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

    form = ParameterForm(True, VPScale)

    if request.method == "POST" and form.validate_on_submit():
        vp_scale = VPScale(id=form.id.data, name=form.name.data)
        db.session.add(vp_scale)
        db.session.commit()

        return redirect(url_for('tournadmin.new_vpscale', page=page))

    page, last_page = pagination_setup(per_page, VPScale)
    vp_scales = VPScale.query.order_by(VPScale.id.asc()).paginate(page=page, per_page=per_page)

    context = {
        'parameters': vp_scales,
        'new_param': True,
        'param_type': ('VP Skala', 'VP Skalen')
    }
    return render_template('', **context)


@tournadmin.route('/vpscale/<int:id>/update', methods=['GET', 'POST'])
@roles_required('Superuser')
def update_vpscale(id):
    pass