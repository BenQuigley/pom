import os

from secret import SECRET_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

HEROKU = os.environ.get('HEROKU')
WTF_CSRF_ENABLED = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')