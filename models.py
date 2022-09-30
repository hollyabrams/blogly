"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL='https://images.app.goo.gl/W6Rnsn5iGPVKALgp7'


# USERS ######################################################################

class User(db.Model):
    __tablename__ = 'users'

    """Sqlalchemy Schema"""
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    # Use cascade to ensure all deleted user posts are also deleted. 
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    @property
    def full_name(self):
        """Method to return full user name"""
        return f'{self.first_name} {self.last_name}'


# POSTS ####################################################################

class Post(db.Model):
    __tablename__ = 'posts'

    """Sqlalchemy Schema"""
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Use strftime to format a datetime into a string"""
        return self.created_at.strftime('%a %b %-d  %Y, %-I:%M %p')


# TAGS ####################################################################

class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')
