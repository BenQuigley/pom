from datetime import datetime
from urllib.parse import urlparse, urljoin

from flask import render_template, flash, redirect, request, abort, url_for, g
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db

from .forms import LoginForm, CreateAccountForm, EditProfileForm, EditPoemForm
from .models import User, Poem

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    poems = Poem.query.order_by(Poem.timestamp.desc()).all()
    return render_template('index.html', poems=poems, verbose=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))
        else:
            flash("I couldn't find that username/password combo.")
    return render_template('login.html',
                           page_title='Sign In',
                           form=form)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.username.data).first()
        if user is not None:
            flash('That username (%s) is taken.' % user.nickname)
        else:
            user = User(nickname=form.username.data,
                        password=form.password.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=form.remember_me.data)

            flash("Account successfully created!")
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))
    else:
        flash_errors(form)
        return render_template('create.html',
                           page_title='Create Account',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user', defaults={'nickname': None})
def user(nickname):
    if nickname is None and g.user is not None and g.user.is_authenticated:
        nickname = g.user.nickname
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    return render_template('user.html', user=user)

@app.route('/poem/<poem_id>')
def poem(poem_id):
    poem = Poem.query.filter_by(id=poem_id).first()
    if poem is None:
        flash('Poem %s not found.' % poem_id)
        return redirect(url_for('index'))
    return render_template('viewPoem.html', poem=poem, verbose=True, poem_main=True)

@app.route('/editpoem/<poem_id>', methods=['GET', 'POST'])
def edit_poem(poem_id):
    form = EditPoemForm()
    poem = Poem.query.filter_by(id=poem_id).first()
    if poem is None:
        flash('Poem %s not found.' % poem_id)
        return redirect(url_for('index'))
    if form.validate_on_submit() and g.user == poem.author:
        if 'delete' in request.form:
            db.session.delete(poem)
            db.session.commit()
            flash('"%s" has been deleted.' % poem.name)
            return redirect(url_for('index'))
        else:
            poem.name = form.name.data
            poem.body = form.body.data
            db.session.add(poem)
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('poem', poem_id=poem.id))
    else:
        flash_errors(form)
        form.name.data = poem.name
        form.body.data = poem.body
        return render_template('editPoem.html', form=form, poem=poem)

@app.route('/newpoem', methods=['GET', 'POST'])
def new_poem():
    form = EditPoemForm()
    if form.validate_on_submit():
        p = Poem(name = form.name.data,
                 body = form.body.data,
                 user_id = g.user.id)
        db.session.add(p)
        db.session.commit()
        flash('Your poem has been published!')
        return redirect(url_for('poem', poem_id=p.id))
    else:
        flash_errors(form)
        return render_template('editPoem.html', form=form)

@app.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    else:
        flash_errors(form)
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('editUser.html', form=form, user=g.user)