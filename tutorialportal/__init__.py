from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from tutorialportal.main.routes import main
    from tutorialportal.tutors.info.routes import tutors_info
    from tutorialportal.tutors.student_manager.routes import tutors_student_manager
    from tutorialportal.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(tutors_info)
    app.register_blueprint(tutors_student_manager)
    app.register_blueprint(errors)

    return app
