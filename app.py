from tutorialportal import create_app, db
from tutorialportal.config import Config

app = create_app(Config)

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all()
