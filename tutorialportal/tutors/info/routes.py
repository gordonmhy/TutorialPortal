from flask import Blueprint, render_template
from flask_login import login_required, current_user

from tutorialportal.config import site_en
from tutorialportal.tutors.info.utils import generate_calender, generate_chart

tutors_info = Blueprint('tutors_info', __name__)


@tutors_info.route('/info')
@login_required
def info():
    calendar = generate_calender(current_user.username)
    monthly_income_chart = {
        24: generate_chart(current_user.username, 24),
        12: generate_chart(current_user.username, 12),
        9: generate_chart(current_user.username, 9),
        6: generate_chart(current_user.username, 6)
    }
    return render_template('tutors/info.html', page_name='Information', site=site_en, calendar=calendar,
                           monthly_income_chart=monthly_income_chart)
