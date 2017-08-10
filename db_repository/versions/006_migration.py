from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
poem = Table('poem', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=120)),
    Column('body', VARCHAR(length=1400)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=120)),
    Column('pwdhash', VARCHAR(length=60)),
    Column('email', VARCHAR(length=120)),
    Column('activate', BOOLEAN),
    Column('created', DATETIME),
    Column('about_me', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['poem'].drop()
    pre_meta.tables['users'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['poem'].create()
    pre_meta.tables['users'].create()
