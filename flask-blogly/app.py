"""Blogly application."""

from flask import Flask, redirect, render_template, request
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True





# app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()
connect_db(app)
db.create_all()


@app.route("/")
def root():   
    """homepage that redirects to list of users"""

    return redirect('/users')



@app.route("/users")
def show_users():
    """show all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)



@app.route("/users/new", methods= ["GET"])
def show_add_form():
    """show form to add new users"""

    return render_template("newuser.html")



@app.route("/users/new", methods=["POST"])
def add_new_user():
    """process add from, add new user and redirect back to /users"""

    new_user = User(
        first_name=request.form["first_name"],
        last_name = request.form["last_name"],
        image_url = request.form["image_url"] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")



@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show info on specific user using user-id"""


    user = User.query.get_or_404(user_id)
    return render_template('show_users.html', user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_page(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_users(user_id):
    """process edit form and update user"""


    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"] or None

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """delete the user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def show_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)

    return render_template("new_post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form["title"],
        content = request.form["content"],
        user = user)
        
    db.session.add(new_post)
    db.session.commit()

    return redirect (f"/users/{user_id}")



@app.route("/posts/<int:post_id>")
def show_posts(post_id):
    """Show a post and buttons to edit and delete the post."""

    post = Post.query.get_or_404(post_id)
    return render_template("show_post.html", post = post)


@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"],
    post.content = request.form["content"]
        
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/users/{post.user_id}')

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """delete the post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect( f"/users/{post.user_id}")


