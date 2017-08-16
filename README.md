# pom

A site for publishing and sharing poetry.

Backend: flask, gunicorn

Frontend: flask-bower, bootstrap

## Online

Pom is hosted on heroku. Visit us at [flask-pom.herokuapp.com](https://flask-pom.herokuapp.com/).

## Installing locally

    $ git clone https://github.com/BenQuigley/pom.git
    $ cd pom
    $ virtualenv flask
    $ source flask/bin/activate
    $ pip install -r requirements.txt
    $ python run.py

## Contributing

Please feel free to add a bug or desired feature to the [bug tracker](https://github.com/BenQuigley/pom/issues),
or to send a pull request.

## Thanks

Pom would not be possible without the excellent documentation from
[Flask](http://flask.pocoo.org/),
[Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/),
[Miguel Grinberg's Flask Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world),
and notes by [Joshua Finnie](https://gist.github.com/joshfinnie) about login management.
