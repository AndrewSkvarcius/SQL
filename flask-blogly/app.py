"""Blogly application."""

from flask import Flask, render_template,redirect,request,flash
from models import db, connect_db, User, Post,PostTag, Tag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
app.debug = True



app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route('/')
def post_home():
    """Show list of recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("poster/post_home.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


# USER Routes


@app.route("/users")
def list_users():
    """List Usrs"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("index.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    """Show Form for new user"""
    
    return  render_template("new.html")
@app.route("/users/new", methods=["POST"])
def new_user():
    """ Handle new user form """
    user_new = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(user_new)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def updated_user(user_id):
    """ Update User handle form sumission"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Delete User handle form submisssion"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

#Post Routes

@app.route('/users/<int:user_id>/posts/new')
def post_create_new(user_id):

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("poster/new.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_create(user_id):

    user= User.query.get_or_404(user_id)
    tag_ids = [int(num) for nums in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user ,tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"{new_post.title} added successfully")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Page with Info on a Post"""

    post = Post.query.get_or_404(post_id)
    return render_template('poster/showing.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('poster/post_edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")

    ####### TAG ROUTES ######

@app.route("/tags")
def tags_home():
    tags = Tag.query.all()
    return render_template('tags/home.html', tags=tags)

@app.route("/tags/new")
def new_tag_form():

    post = Post.query.all()
    return render_template('tags/new.html', post=post)

@app.route("/tags/new", methods = ["POST"])
def new_tag():
    """Form submision for new tags"""

    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)
    
    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}'created")

    return redirect("/tags")

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("tags/edit.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=['POST'])
def edit_tag(tag_id):
    """Form submission for editing tags"""
    
    tag= Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Form submission for deleting tag"""

    tag= Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
