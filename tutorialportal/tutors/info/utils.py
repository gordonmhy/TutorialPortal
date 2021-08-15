import datetime
import base64
from io import BytesIO

from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from tutorialportal.models import Student, Attendance, FeeSubmission

plt.set_loglevel('WARNING')

# WEEKLY TUTORIAL SCHEDULE

def time_to_row(time_lit):
    hour, minute = map(lambda x: int(x), time_lit.split(':'))
    return (hour - 8) * 2 + 1 + (1 if minute == 30 else 0)


def generate_calender(tutor_username):
    # Time allowed: 8:00AM ~ 10:00PM, 30 minutes per slot
    # Days MUST be in the below formats, otherwise insights will be wrong
    day_to_num = {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}
    calendar = [['' for _ in range(8)] for _ in range(29)]  # There are 30 slots per day, 1 slot for title(index)
    for key, value in day_to_num.items():
        calendar[0][value + 1] = key

    def next_time():
        for time in range(36):
            result = '{}:{}0'.format(time // 2 + 8, '3' if time % 2 != 0 else '0')
            yield ('0' if len(result) == 4 else '') + result

    itr = iter(next_time())
    for row in range(1, len(calendar)):
        calendar[row][0] = next(itr)
    students = Student.query.filter_by(tutor_username=tutor_username, active=True).all()
    for student in students:
        row1 = time_to_row(student.lesson_time)
        for row in range(row1, row1 + int(float(student.lesson_duration) * 2)):
            if row <= 0 or row > len(calendar) - 1:
                continue
            for day in list(map(lambda x: int(x), student.lesson_day.split(','))):
                slot = calendar[row][day + 1]
                calendar[row][day + 1] = student.name if slot == '' else calendar[row][day + 1] + ', ' + student.name
    # for i in calendar:
    #     print(i)
    return calendar


# INSIGHTS AND ANALYTICS

# Generates a half-yearly chart by default
def generate_chart(tutor_username, months=6):
    timestamp = datetime.datetime.now()
    year, month = timestamp.year, timestamp.month - 1
    x_axis, y_axis = [], ([], [])
    while not (year == timestamp.year - months // 12 - (1 if months % 12 > timestamp.month else 0) and month == (
            timestamp.month - months - 1) % 12):
        x_axis.append('{}-{}'.format(year, month))
        for line, axis in enumerate(y_axis):
            result = MonthlyData(tutor_username, year, month).get_income_in_month()
            axis.append(result[line])
        month = 12 if month - 1 <= 0 else month - 1
        year = year - 1 if month == 12 else year
    fig = Figure(figsize=(int(months * 0.8), 3))
    ax = fig.subplots()
    # y_label, title, line labels
    labels = ['By Attendance Record', 'By Payment Record']
    for i in range(len(y_axis)):
        ax.plot(x_axis[::-1], y_axis[i][::-1], marker='o', label=labels[i])
    ax.set_ylabel('Income (HKD)')
    ax.set_title('Monthly Income')
    ax.legend()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


class MonthlyData:

    def __init__(self, tutor_username, year, month):
        self.tutor_username = tutor_username
        self.year = year
        self.month = month

    def month_in_range(self, date):
        return int(date.split('-')[0]) == int(self.year) and int(
            date.split('-')[1]) == int(self.month)

    # Returns income by attendance record and by payment record
    def get_income_in_month(self):
        students = Student.query.filter_by(tutor_username=self.tutor_username).all()
        return sum((attendance.lesson_fee
                    for student in students for
                    attendance in Attendance.query.filter_by(username=student.username).all()
                    if self.month_in_range(attendance.lesson_date))), \
               sum((payment.amount for student in students for
                    payment in FeeSubmission.query.filter_by(username=student.username).all() if
                    self.month_in_range(payment.submission_date)))

    def get_monthly_student_count(self):
        return len(set([student.username
                        for student in Student.query.filter_by(tutor_username=self.tutor_username).all()
                        for attendance in Attendance.query.filter_by(username=student.username).all() if
                        int(attendance.lesson_date.split('-')[0]) == int(self.year) and int(
                            attendance.lesson_date.split('-')[1]) == int(self.month)]))
