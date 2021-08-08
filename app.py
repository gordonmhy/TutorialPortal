from tutorialportal import create_app, db
from tutorialportal.config import Config

if __name__ == '__main__':
    create_app(Config).run(debug=True)
    db.create_all()
