from tutorialportal.models import Attendance, FeeSubmission


def get_highlight_count(username, page):
    attendance = Attendance.query.filter_by(username=username).order_by(
        Attendance.lesson_date.desc()).all()
    payment = FeeSubmission.query.filter_by(username=username).all()
    total_owe = sum([a_record.lesson_fee for a_record in attendance])
    total_paid = sum([p_record.amount for p_record in payment])
    owe = total_owe - total_paid
    count = 0
    for a_record in attendance:
        if owe > 0:
            count += 1
        owe -= a_record.lesson_fee
    return count - (page - 1) * 5  # 5 is the paginate per_page number
