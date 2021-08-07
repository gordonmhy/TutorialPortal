from tutorialportal.models import Attendance, FeeSubmission


def get_highlight_count(username, page):
    owe, attendance = get_outstanding_amount(username)
    count = 0
    for a_record in attendance:
        if owe > 0:
            count += 1
        owe -= a_record.lesson_fee
    return count - (page - 1) * 5  # 5 is the paginate per_page number


# month = 13 means all record
def get_invoice_items(username, month=13):
    tmp_owe, attendance = get_outstanding_amount(username)
    total_owe = tmp_owe
    owe = 0
    result = []
    for a_record in attendance:
        if tmp_owe <= 0:
            break
        if month == 13 or int(a_record.lesson_date.split('-')[1]) == month:
            lesson_owe = a_record.lesson_fee if tmp_owe >= a_record.lesson_fee else tmp_owe
            result += [(a_record, lesson_owe)]
            owe += lesson_owe
        tmp_owe -= a_record.lesson_fee
    return total_owe, owe, result


def get_all_invoice_items(username):
    result = []
    for i in range(13):
        result += [get_invoice_items(username, i + 1)]
    return result


def get_outstanding_amount(username):
    attendance = Attendance.query.filter_by(username=username).order_by(
        Attendance.lesson_date.desc()).all()
    payment = FeeSubmission.query.filter_by(username=username).all()
    total_owe = sum([a_record.lesson_fee for a_record in attendance])
    total_paid = sum([p_record.amount for p_record in payment])
    return total_owe - total_paid, attendance
