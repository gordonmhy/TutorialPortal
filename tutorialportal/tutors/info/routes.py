from flask import Blueprint, render_template
from flask_login import login_required, current_user

from tutorialportal.config_test import site
from tutorialportal.tutors.info.utils import generate_calender

tutors_info = Blueprint('tutors_info', __name__)


@tutors_info.route('/info')
@login_required
def info():
    calendar = generate_calender(current_user.username)
    return render_template('tutors/info.html', page_name='Information', site=site)


