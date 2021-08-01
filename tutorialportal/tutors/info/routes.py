from flask import Blueprint, render_template
from flask_login import login_required

from tutorialportal.config_test import site

tutors_info = Blueprint('tutors_info', __name__)


@tutors_info.route('/info')
@login_required
def info():
    return render_template('tutors/info.html', page_name='Information', site=site)


