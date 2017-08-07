from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms import validators

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = StringField('Password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)