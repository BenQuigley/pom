import os

basedir = os.path.abspath(os.path.dirname(__file__))
HEROKU = os.environ.get('HEROKU')

if HEROKU:
    SECRET_KEY = os.environ.get('SECRET_KEY')
else:
    try:
        from secret import SECRET_KEY
    except ImportError:
        SECRET_KEY = "private"

WTF_CSRF_ENABLED = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')