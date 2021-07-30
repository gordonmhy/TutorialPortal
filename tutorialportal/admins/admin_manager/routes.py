from flask import Blueprint
from flask_login import login_required, current_user

admins_admin_manager = Blueprint('admins_admin_manager', __name__)


@admins_admin_manager.route('/manager/admin')
@login_required
def admin_manager():
    if current_user.admin is False:
        return 'access denied'
    return 'Page under construction'
