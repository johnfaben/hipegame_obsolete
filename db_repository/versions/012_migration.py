from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
hipe = Table('hipe', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('hipe', VARCHAR(length=4)),
)

hipe = Table('hipe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('letters', String(length=4)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['hipe'].columns['hipe'].drop()
    post_meta.tables['hipe'].columns['letters'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['hipe'].columns['hipe'].create()
    post_meta.tables['hipe'].columns['letters'].drop()
