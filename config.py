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

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')