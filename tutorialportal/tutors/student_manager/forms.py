from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import datetime
import re


class AddStudentForm(FlaskForm):
    name = StringField('Student Name', render_kw={'placeholder': 'e.g. Peter Chan'},
                       validators=[DataRequired(), Length(max=50)])
    s_phone = StringField('Student\'s phone (Optional)', render_kw={'placeholder': 'e.g. 91234567'})
    p_phone = StringField('Parent\'s phone (Optional)')
    p_rel = StringField('Parent-Child Relationship', render_kw={'placeholder': 'e.g. Mother'},
                        validators=[Length(max=20)])
    lesson_day = StringField('Day(s) of lessons', render_kw={'placeholder': 'e.g. Mon,Thur'},
                             validators=[DataRequired(), Length(min=3, max=30)])
    lesson_time = StringField('Start time of lessons', render_kw={'placeholder': 'e.g. 16:30'},
                              validators=[DataRequired()])
    lesson_duration = FloatField('Duration of lessons (hours)', render_kw={'placeholder': 'e.g. 1.5'},
                                 validators=[DataRequired()])
    lesson_fee = FloatField('Charge per lesson', render_kw={'placeholder': 'e.g. 240'}, validators=[DataRequired()])
    remarks = TextAreaField('Remarks (Optional)', render_kw={'rows': 1})
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


class StudentCredentialsForm(FlaskForm):
    name = StringField('Student Name', render_kw={'placeholder': 'e.g. Peter Chan'},
                       validators=[DataRequired(), Length(max=50)])
    s_phone = StringField('Student\'s phone (Optional)', render_kw={'placeholder': 'e.g. 91234567'})
    p_phone = StringField('Parent\'s phone (Optional)')
    p_rel = StringField('Parent-Child Relationship', render_kw={'placeholder': 'e.g. Mother'},
                        validators=[Length(max=20)])
    lesson_day = StringField('Day(s) of lessons', render_kw={'placeholder': 'e.g. Mon,Thur'},
                             validators=[DataRequired(), Length(min=3, max=30)])
    lesson_time = StringField('Start time of lessons', render_kw={'placeholder': 'e.g. 16:30'},
                              validators=[DataRequired()])
    lesson_duration = FloatField('Duration of lessons (hours)', render_kw={'placeholder': 'e.g. 1.5'},
                                 validators=[DataRequired()])
    lesson_fee = FloatField('Charge per lesson', render_kw={'placeholder': 'e.g. 240'}, validators=[DataRequired()])
    remarks = TextAreaField('Remarks (Optional)', render_kw={'rows': 1})
    student_credentials_submit = SubmitField('Save Changes')

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
                            render_kw={'placeholder': 'e.g. 2021-05-04'}, validators=[DataRequired(message='Invalid date. (YYYY-MM-DD)')])
    lesson_time = StringField('Time', render_kw={'placeholder': 'e.g. 16:30'}, validators=[DataRequired()])
    lesson_duration = StringField('Duration (hrs)', render_kw={'placeholder': 'e.g. 1.5'}, validators=[DataRequired()])
    lesson_fee = FloatField('Charge ($)', render_kw={'placeholder': 'e.g. 400'}, validators=[DataRequired()])
    remarks = TextAreaField('Remarks', render_kw={'rows': 1})
    add_attendance_submit = SubmitField('Submit')

    def validate_lesson_time(self, lesson_time):
        if not re.search('^[012]\d:[0-5]\d$', lesson_time.data):
            raise ValidationError('Invalid lesson time. Must be XX:XX, e.g., 13:30')
