from unittest import TestCase


from app import app
from models import db, User

# create a seperate database for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///for_testing'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
  """Testing User Model"""

  def setUp(self):
    User.query.delete()

  def tearDown(self):
    db.session.rollback()

  def test_get_full_name(self):
    user = User(first_name="Johnny", last_name='Bravo')
    self.assertEqual(user.get_full_name(), 'Johnny Bravo')