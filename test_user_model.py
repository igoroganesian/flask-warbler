"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os

from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from models import db, User

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

TEST_IMAGE_URL = ("https://www.animalfriends.co.uk/siteassets/media/images" +
                 "/article-images/cat-articles/38_afi_article1_caring-for-" +
                 "a-kitten-tips-for-the-first-month.png")

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        # cascade deletes Messages etc.?
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)
        u3 = User.signup("kitten", "kitten@gmail.com",
                         "imkittens", TEST_IMAGE_URL)


        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id
        self.u3_id = u3.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_signup(self):

        u3 = User.query.get(self.u3_id)

        self.assertTrue(bcrypt.check_password_hash(u3.password, "imkittens"))

    def test_signup_fail(self):

        with self.assertRaises(IntegrityError):
            User.signup("kitten", "kitten@gmail.com",
                        "imkittens", TEST_IMAGE_URL)
            db.session.commit()

        with self.assertRaises(ValueError):
            User.signup(None, None, None, None)
            db.session.commit()

    def test_authenticate(self):

        u3 = User.query.get(self.u3_id)

        self.assertEqual(User.authenticate(u3.username, "imkittens"), u3)

    def test_authenticate_fail(self):

        # username doesn't exist
        self.assertFalse(User.authenticate('iamnotakitten', "imkittens"))

        # wrong password
        self.assertFalse(User.authenticate('kitten', "imnotkittens"))

    def test_is_following(self):

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_following(u2))

        u1.following.append(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))

    def test_is_followed_by(self):

        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        self.assertFalse(u1.is_followed_by(u2))

        u1.followers.append(u2)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2))
