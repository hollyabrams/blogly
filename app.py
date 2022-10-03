"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'topsecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """Show recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# USERS #####################################################################

@app.route('/users')
def list_users():
    """Displays a list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users=users)


@app.route('/users/new', methods=['GET'])
def new_user_form():
    """Show an add form for users"""
    return render_template('users/new.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """Process the add form, adding a new user and going back to /users"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f'User {new_user.full_name} added.')
    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_detail(user_id):
    """Show information about the specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show the edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Process the edit form, returning the user to the /users page"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f'User {user.full_name} edited.')

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete the user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.full_name} deleted.')

    return redirect('/users')


# POSTS ############################################################################

@app.route('/users/<int:user_id>/posts/new')
def new_posts_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_posts(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    user = User.query.get_or_404(user_id)
    """getlist returns all values for a key in a form"""
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    flash(f'Post "{new_post.title}" added.')
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_posts(post_id):
    """Handle editing of a post and redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.add(post)
    db.session.commit()
    flash(f'Post "{ post.title }" edited.')
    return redirect(f'/users/{ post.user_id }')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_posts(post_id):
    """Delete the post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post "{ post.title }" deleted.')
    return redirect(f'/users/{ post.user_id }')


# TAGS ###########################################################################

@app.route('/tags')
def tags_list():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)


@app.route('/tags/new')
def new_tags_form():
    """Shows a form to add a new tag"""
    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def new_tags():
    """Process add form, adds tag, and redirect to tag list"""
    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)
    db.session.add(new_tag)
    db.session.commit()
    flash(f'Tag "{ new_tag.name }" added.')
    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """Show detail about a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/detail.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Show edit form for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tags(tag_id):
    """Process edit form, edit tag, and redirects to the tags list"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(tag)
    db.session.commit()
    flash(f'Tag "{ tag.name }" edited.')
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tags(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f'Tag "{ tag.name }" deleted.')
    return redirect('/tags')



    




