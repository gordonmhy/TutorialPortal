from flask import Blueprint, render_template
from flask_login import login_required

from tutorialportal.utils import site

admins_credentials = Blueprint('admins_credentials', __name__)


@admins_credentials.route('/credentials')
@login_required
def credentials():
    return render_template('admins/credentials.html', page_name='Credentials', site=site)


