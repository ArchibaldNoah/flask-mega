import sys

from datetime import datetime, timedelta

import unittest

from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
	def setUp(self):
		print('>>>>>>>>>>>>>>>> test.py: run setup', file=sys.stdout)
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()
		pass

	def tearDown(self):
		print('>>>>>>>>>>>>>>>> test.py: run teardown', file=sys.stdout)
		db.session.remove()
		db.drop_all()
		pass
	
	def test_password_hashing(self):
		u = User(username='susan')
		u.set_password('cat')
		self.assertFalse(u.check_password('dog'))
		self.assertTrue(u.check_password('cat'))

	def test_avatar(self):
		u = User(username='john', email='john@example.com')
		self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'))

	def test_follow(self):
		u1 = User(username='john1', email='john1x@example.com')
		u2 = User(username='john2', email='john2y@example.com')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertEqual(u1.followed.all(),[])
		self.assertEqual(u1.followers.all(),[])

		u1.follow(u2)
		db.session.commit()
		self.assertTrue(u1.is_following(u2))
		self.assertEqual(u1.followed.count(),1)
		self.assertEqual(u2.followers.count(),1)
		self.assertEqual(u2.followers.first().username, 'john1')

if __name__ == '__main__':
	
	unittest.main(verbosity=2)
	#self.teardown()
