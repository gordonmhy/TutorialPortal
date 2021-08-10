from tutorialportal.models import Student


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
    students = Student.query.filter_by(tutor_username=tutor_username).all()
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
