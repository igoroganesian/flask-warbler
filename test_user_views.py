""" Home page view tests """
# python -m unittest test_user_views.py

import os

from unittest import TestCase

# from sqlalchemy.exc import IntegrityError

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app, CURR_USER_KEY

TEST_IMAGE_URL = "https://www.animalfriends.co.uk/siteassets/media/images/article-images/cat-articles/38_afi_article1_caring-for-a-kitten-tips-for-the-first-month.png"

db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    def setUp(self):

        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)
        u3 = User.signup("kitten", "kitten@gmail.com",
                         "imkittens", TEST_IMAGE_URL)

        db.session.add_all([u1, u2, u3])
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id
        self.u3_id = u3.id

    def tearDown(self):
        db.session.rollback()

    def test_logged_in_home(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("homepagetest", html)
            self.assertIn("Log out", html)

    def test_logged_out_home(self):
        with app.test_client() as c:

            resp = c.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign up", html)
            self.assertIn("What's Happening?", html)

    def test_users_list(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@u2", html)
            self.assertIn("@kitten", html)

"""
search
user profile
messages page
followers page
following page
likes page
other user profile
other user messages page
other user's followers page
other user's following page
other user's likes page



"""