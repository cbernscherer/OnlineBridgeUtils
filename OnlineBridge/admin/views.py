from flask import Blueprint, request, render_template, redirect, url_for
from flask_user import roles_required
from OnlineBridge.admin.forms import PlayerUploadForm

admin = Blueprint('admin', __name__, template_folder='templates/admin')

@admin.route('/player_upload', methods=['GET', 'POST'])
@roles_required('Admin')
def player_upload():
    form = PlayerUploadForm()

    if request.method == 'POST' and form.validate_on_submit():

        return redirect(url_for('core.index'))

    return render_template('oebv_players_upload.html', form=form)