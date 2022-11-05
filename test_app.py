from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///for_testing'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
  """Test views of User"""

  def setUp(self):
    """Add sample user data"""

    # This clears the table before running each test
    User.query.delete()

    user = User(first_name='Johnny', last_name='Bravo')
    db.session.add(user)
    db.session.commit()

    self.user_id = user.id
    self.user = user


  def tearDown(self):
    db.session.rollback()


  def test_list_users(self):
    """Testing root route. It should redirect to /users"""

    with app.test_client() as client: 
      #make fake request
      resp = client.get("/users")
      #get data from request
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code,200)

      self.assertIn("Johnny Bravo", html)


  def test_create_user(self):
    """Test creating a new user"""

    with app.test_client() as client:
      d = {"first_name":"Tom", "last_name":"Hank", "image_url":'test.com'}
      resp = client.post('users/new', data=d, follow_redirects=True)
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code,200)
      self.assertIn('<h1>Tom Hank</h1>', html)



  def test_default_image_url(self):
    """Test default value for image_url"""
    with app.test_client() as client:
      d = {"first_name":"spongebob", "last_name":"squarepants", "image_url":""}
      resp = client.post('users/new', data=d, follow_redirects=True)
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code,200)
      self.assertIn('<img src="https://i.pinimg.com/550x/18/b9/ff/18b9ffb2a8a791d50213a9d595c4dd52.jpg" alt="">', html)