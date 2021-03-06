# tournadmin

from flask import Blueprint,request, render_template, redirect, abort, flash, url_for
from flask_user import login_required, roles_required
from OnlineBridge import db
from OnlineBridge.tournadmin.models import VPScale, ScoringMethod, TimeDisplay

tournadmin = Blueprint('tournadmin', __name__, template_folder='templates/tournadmin')


@tournadmin.route('/vpscale/new', methods=['GET', 'POST'])
def new_vpscale():
    pass


@tournadmin.route('/vpscale/<int:id>/update', methods=['GET', 'POST'])
def new_vpscale(id):
    pass