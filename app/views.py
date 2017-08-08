from flask import render_template, flash, redirect, request, abort, url_for, g
from flask_login import login_user, current_user, logout_user, login_required
from app import app
from urllib.parse import urlparse, urljoin
from .forms import LoginForm
from .models import User, Poem

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    poems = Poem.query.order_by(Poem.timestamp).all()
    fake_poems = [ # fake array of posts
        {
            'author': {'nickname': 'iroh'},
            'name': 'They Navigate by Constellation',
            'body': "What tempestuous destiny rushes at them\n"
                    "Who captain their lives, with honor flying as standards,\n"
                    "But with minds as holds, full of millions of worms?\n"
                    "Their houses are full of boxes never unpacked from the move,\n"
                    "That nation of plagiarists,\n"
                    "And the gray glow of computers as they read in bed\n"
                    "Is finally painting their own blue and brown eyes gray.\n"
                    "The indifference of the trees to their ennui,\n"
                    "The swagger of their overfed cats,\n"
                    "The thoughtlessness of what is rotting on the road...\n"
                    "It can swallow a generation; we just know this.\n"
                    "That is its breath they smell when they are microwaving dinner.\n"
                    "Later over the speakers the iPod shuffle-stumbles\n"
                    "To a Segovia waltz or an old song\n"
                    "Their mothers used to sing, as they twist\n"
                    "In the bed sheets together – recalling\n"
                    "The Polaroid memories of their childhoods, but reflecting\n"
                    "How the film for a Polaroid just isn’t made anymore.\n".split('\n')
        },
        {
            'author': {'nickname': 'John'},
            'name': 'omg Portland!',
            'body': ['Beautiful day in Portland!']
        },
        {
            'author': {'nickname': 'Susan'},
            'name': 'Le Film',
            'body': ['The Avengers movie was so cool!']
        }
     ]
    return render_template('index.html',
                           title='Home',
                           poems=poems
                           )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
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
                           title='Sign In',
                           form=form)

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))