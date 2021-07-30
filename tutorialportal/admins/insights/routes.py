from flask import Blueprint
from flask_login import login_required, current_user

admins_insights = Blueprint('admins_insights', __name__)


@admins_insights.route('/insights')
@login_required
def insights():
    if current_user.admin is False:
        return 'access denied'
    return 'Page under construction'
