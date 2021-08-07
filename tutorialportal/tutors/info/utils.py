from tutorialportal.models import Student


def generate_calender(tutor_username):
    # Time allowed: 8:00AM ~ 11:00PM, 30 minutes per slot
    # Days MUST be in the below formats, otherwise insights will be wrong
    day_to_num = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    calendar = [['' for _ in range(8)] for _ in range(31)]  # There are 30 slots per day, 1 slot for title(index)
    students = Student.query.filter_by(tutor_username=tutor_username).all()
