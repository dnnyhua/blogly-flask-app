"""Blogly application."""

from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():


  return redirect("/users")


@app.route('/users')
def list_users():
  """shows list of all users in the database"""

  users = User.query.all()
  return render_template("list.html", users=users)


@app.route('/users/new')
def create_user_form():
  """New user form"""

  return render_template("create_user.html")


@app.route('/users/new', methods=['POST'])
def new_user():
  """Form Submission"""

  first_name = request.form["first_name"]
  last_name = request.form["last_name"]

  # why do we need to put None here?
  image_url = request.form["image_url"] or None

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  db.session.commit()

  return redirect(f"/users/{new_user.id}")


@app.route('/users/<int:user_id>')
def user_profile(user_id):
  """Show user profile"""

  user = User.query.get_or_404(user_id)
  return render_template("user_profile.html",user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
  """Show edit form"""

  user = User.query.get_or_404(user_id)
  return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
  """Update user profile"""

  user = User.query.get_or_404(user_id)

  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url']

  db.session.add(user)
  db.session.commit()

  # why can't i redirect to /users/user_id correctly?
  return redirect(f"/users/{user_id}")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  """Delete user. Will be removed from the database."""

  user = User.query.get_or_404(user_id)

  db.session.delete(user)
  db.session.commit()

  return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
  """Show New Post Form"""

  user = User.query.get_or_404(user_id)

  return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
  """ New post submission """

  user = User.query.get_or_404(user_id)

  title = request.form["title"]
  content = request.form["content"]
  

  new_post = Post(title=title, content=content, user=user)

  db.session.add(new_post)
  db.session.commit()

  return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
  post = Post.query.get(post_id)

  return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):

  post = Post.query.get(post_id)

  return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_update(post_id):

  post = Post.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']
  db.session.add(post)
  db.session.commit()

  return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

  post = Post.query.get(post_id)
  db.session.delete(post)
  db.session.commit()
  
  return redirect(f"/users/{post.user_id}")
