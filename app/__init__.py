import os
from flask import Flask
from config import basedir
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField
from flask_wtf import Form
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Standard Forms

class signup_form(Form):
    username = StringField('Nickname', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    accept_tos = BooleanField('I accept the Terms of Service', [validators.DataRequired()])


from app import views, models