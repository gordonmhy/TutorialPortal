import datetime
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class AddStudentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired(), Length(max=50)])
    s_phone = StringField('Student\'s phone')
    p_phone = StringField('Parent\'s phone')
    p_rel = StringField('Parent-Child Relationship', validators=[Length(max=20)])
    lesson_day = StringField('Day(s) of lessons', validators=[DataRequired(), Length(min=3, max=30)])
    lesson_time = StringField('Start time of Lessons', validators=[DataRequired()])
    lesson_duration = FloatField('Duration of lessons (hours)', validators=[DataRequired()])
    lesson_fee = FloatField('Charge per lesson', validators=[DataRequired()])
    remarks = TextAreaField('Remarks', render_kw={"rows": 1})
    add_student_submit = SubmitField('Submit')

    def validate_name(self, name):
        if not re.search('[\w]+[ ][\w]+[\w ]*', name.data):
            raise ValidationError('Invalid name!')

    def validate_lesson_day(self, lesson_day):
        if not re.search('^([A-Z][a-z]{2,3})([,][A-Z][a-z]{2,3}){0,6}$', lesson_day.data):
            raise ValidationError('Invalid day(s)!  E.g., \'Tue,Thur\'')

    def validate_lesson_time(self, lesson_time):
        if not re.search('^\d{2}:\d{2}$', lesson_time.data):
            raise ValidationError('Invalid lesson start time. Must be XX:XX, e.g., 13:30')

    def validate_s_phone(self, s_phone):
        if not re.search('^[5679]\d{7}$', s_phone.data) and not s_phone.data == '':
            raise ValidationError('Field must be an 8-digit HK phone number.')

    def validate_p_phone(self, p_phone):
        if not re.search('^[5679]\d{7}$', p_phone.data) and not p_phone.data == '':
            raise ValidationError('Field must be an 8-digit HK phone number.')


class AStudentCredentialsForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired(), Length(max=50)])
    s_phone = StringField('Student\'s phone')
    p_phone = StringField('Parent\'s phone')
    p_rel = StringField('Parent-Child Relationship', validators=[Length(max=20)])
    lesson_day = StringField('Day(s) of lessons', validators=[DataRequired(), Length(min=3, max=30)])
    lesson_time = StringField('Start time of Lessons', validators=[DataRequired()])
    lesson_duration = FloatField('Duration of lessons (hours)', validators=[DataRequired()])
    lesson_fee = FloatField('Charge per lesson', validators=[DataRequired()])
    remarks = TextAreaField('Remarks', render_kw={"rows": 1})
    a_student_credentials_submit = SubmitField('Save Changes')

    def validate_name(self, name):
        if not re.search('[\w]+[ ][\w]+[\w ]*', name.data):
            raise ValidationError('Invalid name!')

    def validate_lesson_day(self, lesson_day):
        if not re.search('^([A-Z][a-z]{2,3})([,][A-Z][a-z]{2,3}){0,6}$', lesson_day.data):
            raise ValidationError('Invalid day(s)!  E.g., \'Tue,Thur\'')

    def validate_lesson_time(self, lesson_time):
        if not re.search('^[012]\d:[0-5]\d$', lesson_time.data):
            raise ValidationError('Invalid lesson start time. Must be XX:XX, e.g., 13:30')

    def validate_s_phone(self, s_phone):
        if not re.search('^[5679]\d{7}$', s_phone.data) and not s_phone.data == '':
            raise ValidationError('Field must be an 8-digit HK phone number.')

    def validate_p_phone(self, p_phone):
        if not re.search('^[5679]\d{7}$', p_phone.data) and not p_phone.data == '':
            raise ValidationError('Field must be an 8-digit HK phone number.')


class AddAttendanceForm(FlaskForm):
    lesson_date = DateField('Date', default=datetime.datetime.now().date(), format='%Y-%m-%d',
                            validators=[DataRequired(message='Invalid date. (YYYY-MM-DD)')])
    lesson_time = StringField('Time', validators=[DataRequired()])
    lesson_duration = StringField('Duration (hrs)', validators=[DataRequired()])
    lesson_fee = FloatField('Charge ($)', validators=[DataRequired()])
    remarks = TextAreaField('Remarks', render_kw={"rows": 1})
    add_attendance_submit = SubmitField('Submit')

    def validate_lesson_time(self, lesson_time):
        if not re.search('^[012]\d:[0-5]\d$', lesson_time.data):
            raise ValidationError('Invalid lesson time. Must be XX:XX, e.g., 13:30')
