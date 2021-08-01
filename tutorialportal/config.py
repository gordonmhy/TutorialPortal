# GENERATE 'SECRET_KEY' VIA ANY MEANS YOU PREFER
# DO NOT USE THE DEFAULT SECRET KEY (THIS SERVES AS A TEMPLATE ONLY)

class Config:
    SECRET_KEY = 'o2IlisxsQy7lFEPBUeVjZX75HRy'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'


site = {
    'name': 'Tutorial Portal',
    'a_panels': [
        ('Information and Controls',
         'View all your personal info, tutorial plans, and anything else important in this '
         'panel.', 'tutors_info.info'),
        ('Student Management Panel', 'View, control and manipulate the attendance, tutorial plan, payment history and '
                                     'info of individual students.', 'tutors_student_manager.student_manager')
    ]
}
