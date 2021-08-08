from flask import Blueprint, render_template
from tutorialportal.config import site_en

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('general/errors/404.html', site=site_en), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('general/errors/403.html', site=site_en), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('general/errors/500.html', site=site_en), 500
