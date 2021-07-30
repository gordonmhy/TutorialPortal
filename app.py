from tutorialportal import create_app
from tutorialportal.config import Config

if __name__ == '__main__':
    create_app(Config).run(debug=True)
