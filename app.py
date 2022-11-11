"""Blogly application."""

from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


# User routes

@app.route('/')
def root():

  posts = Post.query.all()

  return render_template("posts/homepage.html", posts=posts)


@app.route('/users')
def list_users():
  """shows list of all users in the database"""

  users = User.query.all()
  return render_template("users/list.html", users=users)


@app.route('/users/new')
def create_user_form():
  """New user form"""

  return render_template("users/create_user.html")


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
  return render_template("users/user_profile.html",user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
  """Show edit form"""

  user = User.query.get_or_404(user_id)
  return render_template('users/edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
  """Update user profile"""

  user = User.query.get_or_404(user_id)

  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url']

  db.session.add(user)
  db.session.commit()

  
  return redirect(f"/users/{user_id}")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  """Delete user. Will be removed from the database."""

  user = User.query.get_or_404(user_id)

  db.session.delete(user)
  db.session.commit()

  return redirect('/users')


##############################################
# Post routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
  """Show New Post Form"""

  user = User.query.get_or_404(user_id)
  tags = Tag.query.all()

  return render_template('posts/new_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
  """ New post submission """

  user = User.query.get_or_404(user_id)
  title = request.form["title"]
  content = request.form["content"]

  # This gets all of the values of the boxes that were checked and converts them to integers because "request" returns a string
  tag_ids = [int(num) for num in request.form.getlist("tags")]

  # Filter tag objects that have ids that matches the list in tag_ids
  tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
  new_post = Post(title=title, content=content, user=user, tags=tags)

  db.session.add(new_post)
  db.session.commit()

  return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
  post = Post.query.get(post_id)

  return render_template('posts/post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
  """ Show post's details. Title, content, user's name, date posted"""

  tags = Tag.query.all()
  post = Post.query.get(post_id)

  return render_template('posts/edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_update(post_id):

  post = Post.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']

  tag_ids =[int(num) for num in request.form.getlist("tags")]
  post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

  db.session.add(post)
  db.session.commit()

  return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

  post = Post.query.get(post_id)
  db.session.delete(post)
  db.session.commit()
  
  return redirect(f"/users/{post.user_id}")
  

###########################################
# Tag routes

@app.route('/tags')
def list_all_tags():
  """" Show a list of all of the tags created """

  tags = Tag.query.all()
  return render_template('tags/list_tags.html', tags=tags)


@app.route('/tags/new')
def new_tag_form():
  """ Show form to add new tags """

  posts = Post.query.all()

  return render_template('tags/new_tag_form.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def new_tag_submit():
  """ Handle form submission for new tags """

  post_ids = [int(num) for num in request.form.getlist("posts")]
  posts = Post.query.filter(Post.id.in_(post_ids)).all()

  name = request.form["name"]
  new_tag = Tag(name=name, posts=posts)
  

  db.session.add(new_tag)
  db.session.commit()

  return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
  """Show detail about tag """

  posts = Post.query.all()
  tag = Tag.query.get(tag_id)

  return render_template('tags/show_tags.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):
  """ Show form to edit tag """

  tag = Tag.query.get(tag_id)

  return render_template('tags/edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tag_edit_submit(tag_id):
  """ Handle edit submission to update tag """

  tag = Tag.query.get(tag_id)
  tag.name = request.form['name']

  db.session.add(tag)
  db.session.commit()

  return redirect(f"/tags/{tag_id}")


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
  """ Delete a tag """

  tag = Tag.query.get(tag_id)
  db.session.delete(tag)
  db.session.commit()

  return redirect('/tags')
