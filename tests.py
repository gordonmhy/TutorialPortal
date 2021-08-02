# Directly execute this file using 'python tests.py' via your terminal

import unittest
import app

from tutorialportal import db, bcrypt
from tutorialportal.config import Config
from tutorialportal.models import User, Student, Tutor, Attendance


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

        print("Initializing dummy data...")

        # TEST TUTOR 1

        test_tutor_1_user = User(username='test_tutor_1', tutor=True)
        test_tutor_1_user.password = bcrypt.generate_password_hash('password ...').decode()
        db.session.add(test_tutor_1_user)

        test_tutor_1_tutor = Tutor(username='test_tutor_1', name='Test Tutor One', email='test_tutor_1@email.com')
        db.session.add(test_tutor_1_tutor)

        # TEST TUTOR 2

        test_tutor_2_user = User(username='test_tutor_2', tutor=True)
        test_tutor_2_user.password = bcrypt.generate_password_hash('password ...').decode()
        db.session.add(test_tutor_2_user)

        test_tutor_2_tutor = Tutor(username='test_tutor_2', name='Test Tutor Two', email='test_tutor_2@email.com',
                                   remark='test remark')
        db.session.add(test_tutor_2_tutor)

        # TEST STUDENT 1 (Student of Tutor 1)

        test_student_1_user = User(username='test_student_1', tutor=False)
        test_student_1_user.password = bcrypt.generate_password_hash('password ...').decode()
        db.session.add(test_student_1_user)

        test_student_1_student = Student(username='test_student_1', name='Test Student One', s_phone='66666666',
                                         p_phone='999999999', p_rel='Mother', lesson_day='Mon,Thur',
                                         lesson_time='13:00', lesson_duration='3.0', lesson_fee=400.0,
                                         tutor_username=test_tutor_1_user.username, remark='test remark')
        db.session.add(test_student_1_student)

        # TEST STUDENT 2 (Student of Tutor 1)

        test_student_2_user = User(username='test_student_2', tutor=False)
        test_student_2_user.password = bcrypt.generate_password_hash('password ...').decode()
        db.session.add(test_student_2_user)

        test_student_2_student = Student(username='test_student_2', name='Test Student Two', s_phone='999999999',
                                         lesson_day='Mon,Thur', lesson_time='18:30', lesson_duration='2',
                                         lesson_fee=100.0, tutor_username=test_tutor_1_user.username,
                                         active=False, remark='test remark')
        db.session.add(test_student_2_student)

        # TEST STUDENT 3 (Student of Tutor 2)

        test_student_3_user = User(username='test_student_3', tutor=False)
        test_student_3_user.password = bcrypt.generate_password_hash('password ...').decode()
        db.session.add(test_student_3_user)

        test_student_3_student = Student(username='test_student_3', name='Test Student Three',
                                         lesson_day='Mon,Thur',
                                         lesson_time='13:00', lesson_duration='1.5', lesson_fee=285.0,
                                         tutor_username=test_tutor_2_user.username)
        db.session.add(test_student_3_student)

        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        print("Deleting dummy data...")
        db.session.delete(User.query.get('test_tutor_1'))
        db.session.delete(Tutor.query.get('test_tutor_1'))
        db.session.delete(User.query.get('test_tutor_2'))
        db.session.delete(Tutor.query.get('test_tutor_2'))
        db.session.delete(User.query.get('test_student_1'))
        db.session.delete(Student.query.get('test_student_1'))
        db.session.delete(User.query.get('test_student_2'))
        db.session.delete(Student.query.get('test_student_2'))
        db.session.delete(User.query.get('test_student_3'))
        db.session.delete(Student.query.get('test_student_3'))
        db.session.commit()

    def test_record(self):
        print("Testing record correctness...")
        self.assertIsNotNone(User.query.get('test_tutor_1'))
        self.assertIsNotNone(Student.query.filter_by(username='test_student_1'))
        self.assertIsNone(Tutor.query.get('test_student_2'))

    def test_relation(self):
        # test_tutor_1 should only have one active student which is test_student_1
        print("Testing student-to-tutor relationship...")
        self.assertEqual(
            next(iter([student.username for student in Student.query.filter_by(tutor_username='test_tutor_1') if
                       student.active is True]), None), 'test_student_1')

    def test_attendance(self):
        print("Testing attendance...")

        test_attendance_1 = Attendance(username='test_student_1', lesson_date='2021-08-02', lesson_time='14:30',
                                       lesson_duration='1', lesson_fee=200.0)
        db.session.add(test_attendance_1)
        test_attendance_2 = Attendance(username='test_student_3', lesson_date='2021-08-02', lesson_time='14:30',
                                       lesson_duration='2', lesson_fee=250.0)
        db.session.add(test_attendance_2)
        test_attendance_3 = Attendance(username='test_student_2', lesson_date='2021-08-02', lesson_time='18:30',
                                       lesson_duration='2.5', lesson_fee=200.0)
        db.session.add(test_attendance_3)
        db.session.commit()

        self.assertEqual(next(iter([attendance.username for attendance in Attendance.query.all() if Student.query.get(
            attendance.username).tutor_username == 'test_tutor_1' and Student.query.get(
            attendance.username).active is False]), None), 'test_student_2')

        db.session.delete(Attendance.query.filter_by(username='test_student_1')[0])
        db.session.delete(Attendance.query.filter_by(username='test_student_2')[0])
        db.session.delete(Attendance.query.filter_by(username='test_student_3')[0])
        db.session.commit()


if __name__ == '__main__':
    with app.create_app(Config).app_context():
        unittest.main()
