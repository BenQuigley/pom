from datetime import datetime

from app import db, login_manager
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

# Standard Databases

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(120), index=True, unique=True)
    pwdhash = db.Column(db.String(60))
    poems = db.relationship('Poem', backref='author', lazy='dynamic')
    email = db.Column(db.String(120), index=True, unique=False)
    activate = db.Column(db.Boolean)
    created = db.Column(db.DateTime)

    def __init__(self, nickname, password, email=None):
        self.nickname = nickname
        self.pwdhash = generate_password_hash(password)
        self.email = email
        self.activate = False
        self.created = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # Python 2
        except NameError:
            return str(self.id) # Python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1400))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))