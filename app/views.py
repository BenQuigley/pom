from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'iroh'}  # fake user
    poems = [ # fake array of posts
        {
            'author': {'nickname': 'iroh'},
            'name': 'They Navigate by Constellation',
            'body': ["What tempestuous destiny rushes at them",
                    "Who captain their lives, with honor flying as standards,",
                    "But with minds as holds, full of millions of worms?",
                    "Their houses are full of boxes never unpacked from the move,",
                    "That nation of plagiarists,",
                    "And the gray glow of computers as they read in bed",
                    "Is finally painting their own blue and brown eyes gray.",
                    "The indifference of the trees to their ennui,",
                    "The swagger of their overfed cats,",
                    "The thoughtlessness of what is rotting on the road...",
                    "It can swallow a generation; we just know this.",
                    "That is its breath they smell when they are microwaving dinner.",
                    "Later over the speakers the iPod shuffle-stumbles",
                    "To a Segovia waltz or an old song",
                    "Their mothers used to sing, as they twist",
                    "In the bed sheets together – recalling",
                    "The Polaroid memories of their childhoods, but reflecting",
                    "How the film for a Polaroid just isn’t made anymore."],
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
                           user=user,
                           poems=poems
                           )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])