"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image_url = "https://i.pinimg.com/550x/18/b9/ff/18b9ffb2a8a791d50213a9d595c4dd52.jpg"

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  """User table"""

  __tablename__= 'users'


  def __repr__(self):
    u = self
    return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>" 


  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.Text, nullable=False)
  last_name = db.Column(db.Text, nullable=False)
  image_url = db.Column(db.Text, nullable=False, default=default_image_url)

  def get_full_name(self):
    """Gets first and last name"""
    return f'{self.first_name} {self.last_name}'