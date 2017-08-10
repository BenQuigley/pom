from datetime import datetime
from hashlib import md5

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from config import HEROKU
from app import db, login_manager

# Database model for site users.

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(120), index=True, unique=True)
    pwdhash = db.Column(db.String(60))
    poems = db.relationship('Poem', backref='author', lazy='dynamic')
    email = db.Column(db.String(120), index=True, unique=False)
    activate = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def __init__(self, nickname, password, email=None):
        self.nickname = nickname
        self.pwdhash = generate_password_hash(password)
        self.email = email
        self.activate = False
        self.created = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def avatar(self, size=64):
        return 'https://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    @property
    def is_authenticated(self):
        return True

    @property
    def last_seen_display(self):
        return str(self.last_seen).split('.')[0]

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # Python 2
        except NameError:
            return str(self.id) # Python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

# Database model for user poems.

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    body = db.Column(db.String(1400))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, body, user_id):
        self.name = name
        self.body = body
        self.user_id = user_id
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Post %r>' % (self.body)

    @property
    def body_lines(self):
        return self.body.split("\n")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if HEROKU:
    from test_data import user, poem
    db.create_all()
    db.session.add(user)
    db.session.add(poem)
    db.session.commit()