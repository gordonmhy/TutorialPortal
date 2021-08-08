# GENERATE 'SECRET_KEY' VIA ANY MEANS YOU PREFER
# DO NOT USE THE DEFAULT SECRET KEY (THIS SERVES AS A TEMPLATE ONLY)

class Config:
    SECRET_KEY = 'o2IlisxsQy7lFEPBUeVjZX75HRy'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'


supported_languages = ['en', 'zh']

site_en = {
    'name': 'Tutorial Portal',
    'a_panels': [
        ('Information and Controls',
         'View all your personal information, weekly tutorial schedule and generated insights such as charts, '
         'aggregated data and decision-driving info on this panel.',
         'tutors_info.info'),
        ('Student Management Panel',
         'View, control and manipulate the attendance, tutorial plan, payment history and credentials of individual '
         'students.',
         'tutors_student_manager.student_manager')
    ],
    'intro_des': 'This is a demo web application. You may start by navigating to the Register(Tutor) page, create an '
                 'account, login and begin exploring. You are encouraged to report any issues you experience or '
                 'even contribute to this project via Github. You can always click the bottom copyright tag to get to '
                 'the Github repository of this project. '
}

site_zh = {
    'name': '私補學生管理平台',
    'a_panels': [
        ('資訊及管理版面',
         '閱覽及管控你的個人資料、每週私補行程，以及觀看電腦生成的圖表及數據，幫助你作出更明智的決策。',
         'tutors_info.info'),
        ('學生管理版面',
         '閱覽及管控你各個學生的課堂出席狀況、學費付款紀錄，以及其個人資料、補習時數及費用等情況。',
         'tutors_student_manager.student_manager')
    ]
}
