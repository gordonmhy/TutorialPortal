import datetime
import random
from flask import render_template, redirect, url_for, flash, request, abort
from tutorialportal import app, db, bcrypt
from tutorialportal.utils import site
from tutorialportal.forms import LoginForm, AddStudentForm, AStudentCredentialsForm, AddAttendanceForm
from tutorialportal.models import User, Admin, Student, Attendance, FeeSubmission
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            return redirect(next_page if next_page else url_for('home'))
        flash('* Incorrect username or password', 'danger')
    return render_template('login.html', page_name='Login', form=form, site=site)


@app.route('/logout')
def logout():
    logout_user()
    flash('* You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/manager/student', methods=['POST', 'GET'])
@app.route('/manager/student_<string:page>', methods=['POST', 'GET'])
@login_required
def student_manager(page=None):
    if current_user.admin is False:
        abort(403)
    active_students = [(student_record.username, student_record.name) for student_record in
                       Student.query.all() if student_record.active]
    inactive_students = [(student_record.username, student_record.name) for student_record in
                         Student.query.all() if not student_record.active]
    add_student_form = AddStudentForm()
    panel_active = {
        'add_student': False,
        'select_student': False
    }
    if page and page in panel_active.keys():
        panel_active[page] = True
    if request.method == 'GET' and page is None:
        panel_active['select_student'] = True
    if add_student_form.add_student_submit.data:
        if add_student_form.validate_on_submit():
            username = add_student_form.name.data.split(" ")[0].lower() + datetime.datetime.now().strftime('%S%M%H')
            password = add_student_form.name.data.replace(" ", "") + str(random.randint(10, 100))
            user = User(username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'),
                        admin=False)
            db.session.add(user)
            student = Student(username=username, name=add_student_form.name.data, s_phone=add_student_form.s_phone.data,
                              p_phone=add_student_form.p_phone.data, p_rel=add_student_form.p_rel.data,
                              lesson_day=add_student_form.lesson_day.data, lesson_time=add_student_form.lesson_time.data
                              , lesson_duration=add_student_form.lesson_duration.data,
                              lesson_fee=add_student_form.lesson_fee.data, remark=add_student_form.remarks.data,
                              active=True)
            db.session.add(student)
            db.session.commit()
            flash('Student added.\nUsername: {}\nPassword: {}'.format(username, password), 'success')
            return redirect(url_for('student_manager', student_username=username))
        if page is None:
            panel_active['add_student'] = True
    return render_template('student_manager.html', page_name='Student Manager', add_student_form=add_student_form,
                           site=site, panel_active=panel_active, active_students=active_students,
                           inactive_students=inactive_students)


@app.route('/manager/student/<string:student_username>', methods=['POST', 'GET'])
@app.route('/manager/student/<string:student_username>/<string:page>', methods=['POST', 'GET'])
@login_required
def student_manager_selected(student_username, page=None):
    if current_user.admin is False:
        abort(403)
    # Credentials Form, Add Attendance Form,
    # Add Payment Form, Attendance Table with controls, Payment History with controls
    panel_active = {
        'credentials': False,
        'attendance': False,
        'payment': False
    }
    if page and page in panel_active.keys():
        panel_active[page] = True
    if request.method == 'GET' and page is None:
        panel_active['attendance'] = True
    student = Student.query.filter_by(username=student_username).first_or_404()
    a_student_credentials_form = AStudentCredentialsForm()
    add_attendance_form = AddAttendanceForm()
    if a_student_credentials_form.a_student_credentials_submit.data:
        if a_student_credentials_form.validate_on_submit():
            student.name = a_student_credentials_form.name.data
            student.s_phone = a_student_credentials_form.s_phone.data
            student.p_phone = a_student_credentials_form.p_phone.data
            student.p_rel = a_student_credentials_form.p_rel.data
            student.lesson_day = a_student_credentials_form.lesson_day.data
            student.lesson_time = a_student_credentials_form.lesson_time.data
            student.lesson_duration = a_student_credentials_form.lesson_duration.data
            student.lesson_fee = a_student_credentials_form.lesson_fee.data
            student.remark = a_student_credentials_form.remarks.data
            db.session.commit()
            flash('Credentials updated for {}.'.format(student.name), 'success')
        if page is None:
            panel_active['credentials'] = True
    elif add_attendance_form.add_attendance_submit.data:
        if add_attendance_form.validate_on_submit():
            # Possibly add a check in timeslot overlapping
            attendance = Attendance(username=student.username, lesson_date=add_attendance_form.lesson_date.data,
                                    lesson_time=add_attendance_form.lesson_time.data,
                                    lesson_fee=add_attendance_form.lesson_fee.data,
                                    lesson_duration=add_attendance_form.lesson_duration.data,
                                    remark=add_attendance_form.remarks.data)
            db.session.add(attendance)
            db.session.commit()
            flash('Attendance added for {}.'.format(student.name), 'success')
        else:
            flash('Some of your input may be invalid.', 'danger')
        if page is None:
            panel_active['attendance'] = True
    else:
        if page is None:
            panel_active['attendance'] = True
        a_student_credentials_form.name.data = student.name
        a_student_credentials_form.s_phone.data = student.s_phone
        a_student_credentials_form.p_phone.data = student.p_phone
        a_student_credentials_form.p_rel.data = student.p_rel
        a_student_credentials_form.lesson_day.data = student.lesson_day
        a_student_credentials_form.lesson_time.data = student.lesson_time
        a_student_credentials_form.lesson_duration.data = student.lesson_duration
        a_student_credentials_form.lesson_fee.data = student.lesson_fee
        a_student_credentials_form.remarks.data = student.remark
        add_attendance_form.lesson_time.data = student.lesson_time
        add_attendance_form.lesson_duration.data = student.lesson_duration
        add_attendance_form.lesson_fee.data = student.lesson_fee
    # Student Attendance Record
    attendance_page = request.args.get('p', 1, type=int)
    student_attendance = Attendance.query.filter_by(username=student.username).order_by(
        Attendance.lesson_date.desc()).paginate(page=attendance_page, per_page=7)
    return render_template('student_manager_selected.html', page_name='Student Manager', site=site,
                           panel_active=panel_active, student=student,
                           a_student_credentials_form=a_student_credentials_form,
                           add_attendance_form=add_attendance_form, student_attendance=student_attendance)


@app.route('/manager/admin')
@login_required
def admin_manager():
    if current_user.admin is False:
        return 'access denied'
    return 'Page under construction'


@app.route('/insights')
@login_required
def insights():
    if current_user.admin is False:
        return 'access denied'
    return 'Page under construction'


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html', page_name='Home', site=site)


@app.route('/credentials')
@login_required
def credentials():
    return render_template('credentials.html', page_name='Credentials', site=site)


@app.route('/make_inactive/<string:student_username>')
@login_required
def make_inactive(student_username):
    if current_user.admin is False:
        abort(403)
    student = Student.query.get(student_username)
    if student:
        student.active = False
        db.session.commit()
        flash('Student {} has been made inactive.'.format(student.name), 'success')
        return redirect(url_for('student_manager_selected', student_username=student_username, page='credentials'))
    abort(403)


@app.route('/make_active/<string:student_username>')
@login_required
def make_active(student_username):
    if current_user.admin is False:
        abort(403)
    student = Student.query.get(student_username)
    if student:
        student.active = True
        db.session.commit()
        flash('Student {} has been made active.'.format(student.name), 'success')
        return redirect(url_for('student_manager_selected', student_username=student_username, page='credentials'))
    abort(403)


@app.route('/remove/student/<string:student_username>', methods=['POST'])
@login_required
def remove_student(student_username):
    if current_user.admin is False:
        abort(403)
    student = Student.query.get(student_username)
    user = User.query.get(student_username)
    if student:
        name = student.name
        db.session.delete(student)
        db.session.delete(user)
        db.session.commit()
        flash('Student {} deleted.'.format(name), 'success')
        return redirect(url_for('student_manager'))
    abort(403)
