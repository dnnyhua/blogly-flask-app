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

  posts = db.relationship("Post", backref="user")

  # Can also use property decorator like the example below so you can use get_full_name instead  of get_full_name()
  def get_full_name(self):
    """Gets first and last name"""
    return f'{self.first_name} {self.last_name}'

  
  # @property
  #   def full_name(self):
  #       """Return full name of user."""

  #       return f"{self.first_name} {self.last_name}"  


class Post(db.Model):
  """ Post made by user """

  __tablename__='posts'

  def __repr__(self):
    p = self
    return f"<Post Id={p.id} title={p.title} content={p.content} created_at={p.created_at}>" 

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=db.func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  # relationships so you can see the .tags for a post, and the .posts for a tag
  # tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

  @property
  def friendly_date(self):
    """Return nicely-formatted date."""

    return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
  """Tags to use on post"""

  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text, nullable=False, unique=True)

  posts = db.relationship('Post', secondary='posts_tags', backref='tags')



class PostTag(db.Model):
  """Joins Post and Tag"""
  
  __tablename__  = 'posts_tags'

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)