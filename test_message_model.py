"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os

from unittest import TestCase

from models import db, User, Message

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    def setUp(self):
        # cascade deletes Messages etc.?
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        m1 = Message(text='I am message1')
        u1.messages.append(m1)

        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        self.m1_id = m1.id

    def tearDown(self):
        db.session.rollback()

    def test_create_message(self):

        m1 = Message.query.get(self.m1_id)
        u1 = User.query.get(self.u1_id)

        # which one is better?
        self.assertEqual(m1.text,'I am message1')
        self.assertEqual(u1.messages[0].text,'I am message1')

        self.assertEqual(len(u1.messages), 1)

    def test_delete_message(self):

        m1 = Message.query.get(self.m1_id)
        u1 = User.query.get(self.u1_id)

        db.session.delete(m1)
        db.session.commit()

        self.assertIsNone(Message.query.get(self.m1_id))
        self.assertEqual(len(u1.messages), 0)


    def test_liked_message(self):

        m1 = Message.query.get(self.m1_id)
        u2 = User.query.get(self.u2_id)

        u2.liked_messages.append(m1)

        db.session.commit()

        self.assertEqual(u2.liked_messages[0].text, 'I am message1')
        self.assertEqual(len(u2.liked_messages), 1)

        u2.liked_messages.remove(m1)

        db.session.commit()

        self.assertEqual(len(u2.liked_messages), 0)