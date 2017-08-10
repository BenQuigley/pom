import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app import views, models

if not app.debug:
    import logging
    if os.environ.get('HEROKU'):
        stream_handler = logging.StreamHandler()
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('pom startup')
    else:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('tmp/pom.log', 'a', 1*1024*1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s: [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('pom startup')

if __name__ == '__main__':
    from test_data import user, poem
    db.create_all()
    db.session.add(user)
    db.session.add(poem)
    db.session.commit()