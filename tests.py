#!/Users/faben/anaconda/bin/python

import os
import unittest
from datetime import datetime,timedelta

from config import basedir
from app import app, db
from app.models import User,Post

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(username = 'dave', email = 'john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_follow(self):
        u = User(username = 'Alice', email = 'alice@alice.com')
        v = User(username = 'Bob',email = 'bob@bob.com')
        w = User(username = 'Charlie',email = 'charlie@charlie.com')
        x = User(username = 'Eve', email = 'eve@eve.com')
        db.session.add(u)
        db.session.add(v)
        db.session.add(w)
        db.session.add(x)

        # make a post for each user
        utcnow = datetime.utcnow()

        p1 = Post(body = 'post from Alice', author = u,timestamp = utcnow+timedelta(seconds=1))
        p2 = Post(body = 'post from Bob', author = v,timestamp = utcnow+timedelta(seconds=2))
        p3 = Post(body = 'post from Charlie', author = w,timestamp = utcnow+timedelta(seconds=3))
        p4 = Post(body = 'post from Eve', author = x,timestamp = utcnow+timedelta(seconds=4))

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()

        assert u.unfollow(v) is None
        u.follow(u)
        u.follow(v)
        u.follow(x)
        v.follow(v)
        v.follow(w)
        w.follow(w)
        w.follow(x)
        x.follow(x)
        db.session.add(u)
        db.session.add(v)
        db.session.add(w)
        db.session.add(x)
        db.session.commit()

        f1 = u.followed_posts().all()
        f2 = v.followed_posts().all()
        f3 = w.followed_posts().all()
        f4 = x.followed_posts().all()

        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1

        assert f1 == [p4,p2,p1]
        assert f2 == [p3,p2]






if __name__ == '__main__':
    unittest.main()
