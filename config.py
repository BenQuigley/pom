# Whoosh does not work on Heroku

import os

WHOOSH_ENABLED = os.environ.get('HEROKU') is None