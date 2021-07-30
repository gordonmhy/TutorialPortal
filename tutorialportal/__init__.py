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
    from tutorialportal.admins.credentials.routes import admins_credentials
    from tutorialportal.admins.student_manager.routes import admins_student_manager
    from tutorialportal.admins.admin_manager.routes import admins_admin_manager
    from tutorialportal.admins.insights.routes import admins_insights

    app.register_blueprint(main)
    app.register_blueprint(admins_credentials)
    app.register_blueprint(admins_student_manager)
    app.register_blueprint(admins_admin_manager)
    app.register_blueprint(admins_insights)

    return app
