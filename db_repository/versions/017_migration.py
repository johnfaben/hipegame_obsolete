from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('about_me', VARCHAR(length=140)),
    Column('last_seen', DATETIME),
    Column('social_id', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('email', String(length=120)),
    Column('about_me', String(length=140)),
    Column('last_seen', DateTime),
)

solvers = Table('solvers', post_meta,
    Column('solver_id', Integer),
    Column('hipe_id', Integer),
    Column('score', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['nickname'].drop()
    pre_meta.tables['user'].columns['social_id'].drop()
    post_meta.tables['user'].columns['username'].create()
    post_meta.tables['solvers'].columns['score'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['nickname'].create()
    pre_meta.tables['user'].columns['social_id'].create()
    post_meta.tables['user'].columns['username'].drop()
    post_meta.tables['solvers'].columns['score'].drop()
