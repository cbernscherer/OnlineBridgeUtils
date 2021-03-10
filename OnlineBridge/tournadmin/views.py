# tournadmin
from flask import Blueprint,request, render_template, redirect, abort, flash, url_for
from flask_user import login_required, roles_required, current_user
from OnlineBridge import db
from OnlineBridge.tournadmin.models import VPScale, ScoringMethod, TimeDisplay
from OnlineBridge.tournadmin.forms import ParameterForm
from utilities import pagination_setup

tournadmin = Blueprint('tournadmin', __name__, template_folder='templates/tournadmin')

def get_param_model(param_type):
    model = None
    show_tourn_type = False
    param_type_str = None

    if param_type == 'vp_scale':
        model = VPScale
        param_type_str = ('VP Skala', 'VP Skalen', 'vp_scale')
    elif param_type == 'time_display':
        model = TimeDisplay
        param_type_str = ('Zeitanzeige', 'Zeitanzeigen', 'time_display')
    elif param_type =='scoring_method':
        model = ScoringMethod
        param_type_str = ('Scoremethode', 'Scoremethoden', 'scoring_method')
        show_tourn_type = True

    if model is None:
        abort(404)

    return model, param_type_str, show_tourn_type


@tournadmin.route('/parameter/<string:param_type>/new', methods=['GET', 'POST'])
@roles_required('Superuser')
def new_param(param_type):
    per_page = 10

    model, param_type_str, show_tourn_type = get_param_model(param_type)

    page, last_page = pagination_setup(per_page, model)

    form = ParameterForm(True, model, -1)

    if request.method == "POST" and form.validate_on_submit():
        parameter = model(id=form.id.data, name=form.name.data)
        if show_tourn_type:
            parameter.tournament_type = form.tournament_type.data

        db.session.add(parameter)
        db.session.commit()

        return redirect(url_for('tournadmin.new_param', page=page))

    parameters = model.query.order_by(model.id.asc()).paginate(page=page, per_page=per_page)

    context = {
        'form': form,
        'parameters': parameters,
        'show_tourn_type': show_tourn_type,
        'new_param': False,
        'param_type': param_type_str
    }
    return render_template('parameter.html', **context)


@tournadmin.route('/parameter/<string:param_type>/<int:id>/update', methods=['GET', 'POST'])
@roles_required('Superuser')
def update_paramm(param_type ,id):
    per_page = 10

    model, param_type_str, show_tourn_type = get_param_model(param_type)

    page, last_page = pagination_setup(per_page, model)

    parameter = model.query.filter_by(id=id).first_or_404()

    form = ParameterForm(False, model, parameter.id)

    if request.method == "POST" and form.validate_on_submit():
        parameter.name = form.name.data
        if show_tourn_type:
            parameter.tournament_type = form.tournament_type.data

        db.session.add(parameter)
        db.session.commit()

        return redirect(url_for('tournadmin.new_param', page=page, param_type=param_type))

    elif request.method == 'GET':
        form.name.data = parameter.name
        if show_tourn_type:
            form.tournament_type.data = parameter.tournament_type

    form.id.data = parameter.id
    parameters = model.query.order_by(model.id.asc()).paginate(page=page, per_page=per_page)

    context = {
        'form': form,
        'parameters': parameters,
        'this_param': parameter,
        'show_tourn_type': show_tourn_type,
        'new_param': False,
        'param_type': param_type_str
    }
    return render_template('parameter.html', **context)


@tournadmin.route('/parameter/<string:param_type>/<int:id>/delete', methods=['GET'])
@roles_required('Superuser')
def param_delete(param_type, id):
    if request.method == 'GET':
        model, param_type_str, show_tourn_type = get_param_model(param_type)

        parameter = model.query.filter_by(id=id).first_or_404()
        db.session.delete(parameter)
        db.session.commit()

    return redirect(url_for('tournadmin.new_param', param_type=param_type))