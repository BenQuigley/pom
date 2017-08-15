import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bower import Bower

from config import basedir, HEROKU

app = Flask(__name__)
Bower(app)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import logging
if HEROKU:
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.ERROR)
    app.logger.info('pom startup')
elif not app.debug:
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/pom.log', 'a', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s: [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('pom startup')

from app import views, models