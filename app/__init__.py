import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bower import Bower

from config import HEROKU

""" Create and configure the application and database. """
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

""" Initialize the frontend library manager. """
Bower(app)

""" Initialize the login manager. """
login_manager = LoginManager()
login_manager.init_app(app)

""" Set up the logging modes. """
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

""" Run the next modues, populating the application with views and models. """
from app import views, models