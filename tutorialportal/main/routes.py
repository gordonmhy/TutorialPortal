from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required

from tutorialportal.main.forms import LoginForm
from tutorialportal.models import User
from tutorialportal.config_test import site
from tutorialportal import bcrypt

import random

main = Blueprint('main', __name__)


@main.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        user_not_found = False
        dummy = bcrypt.generate_password_hash(form.password.data + str(random.random())).decode('utf-8')
        if user is None:
            user_not_found = True
        if bcrypt.check_password_hash(user.password if not user_not_found else dummy, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.home'))
        flash('* Incorrect username or password', 'danger')
    return render_template('general/login.html', page_name='Login', form=form, site=site)


@main.route('/logout')
def logout():
    logout_user()
    flash('* You have been logged out.', 'success')
    return redirect(url_for('main.login'))


@main.route('/')
@main.route('/home')
@login_required
def home():
    return render_template('general/home.html', page_name='Home', site=site)
