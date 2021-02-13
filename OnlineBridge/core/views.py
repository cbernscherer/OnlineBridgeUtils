# under core

from flask import Blueprint, render_template

core = Blueprint('core', __name__, template_folder='templates/core')

@core.route('/')
def index():
    return render_template('index.html')

@core.route('/about')
def about():
    return render_template('about.html')

@core.route('/impressum')
def impressum():
    return render_template('impressum.html')

@core.route('/data_protection')
def data_protection():
    return render_template('ds.html')