from flask import Blueprint, render_template
from flask_login import login_required

from tutorialportal.config_test import site

admins_info = Blueprint('admins_info', __name__)


@admins_info.route('/info')
@login_required
def info():
    return render_template('admins/info.html', page_name='Information', site=site)


