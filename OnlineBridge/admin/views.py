from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_user import roles_required
from OnlineBridge.admin.forms import PlayerUploadForm
from utilities.populate_db import fed_members_upload

admin = Blueprint('admin', __name__, template_folder='templates/admin')

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