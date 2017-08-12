from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms import validators

class LoginForm(FlaskForm):

    username = StringField('Username', [validators.DataRequired("Username is required.")])
    password = PasswordField('Password', [validators.DataRequired("Password is required.")])
    remember_me = BooleanField('Remember me', default=False)

class CreateAccountForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired("Username is required."),
                                        validators.Length(min=4, max=16)])
    email = StringField('Email', [validators.DataRequired("Email is required."),
                                  validators.Email(message="Email must be an email."),
                                  validators.Length(min=0, max=120)])
    password = PasswordField('Password', [validators.DataRequired("Password is required.")])
    password_confirm = PasswordField('Password confirm',
                                     [validators.DataRequired("Password confirmation is required."),
                                      validators.EqualTo('password', message="Passwords must match.")])
    remember_me = BooleanField('Remember me', default=False)

class EditProfileForm(FlaskForm):
    nickname = StringField('nickname', [validators.DataRequired()])
    about_me = TextAreaField('about_me', [validators.Length(min=0, max=140)])

class EditPoemForm(FlaskForm):
    body = TextAreaField('body', [validators.Length(min=0, max=140)])
    about_me = TextAreaField('about_me', [validators.Length(min=0, max=1400)])