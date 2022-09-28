"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL='https://images.app.goo.gl/pwHVKVwAh6t97iU99'

class User(db.Model):
    __tablename__ = 'users'

    """Sqlalchemy Schema"""
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)


    @property
    def full_name(self):
        """Method to return full user name"""
        return f'{self.first_name} {self.last_name}'
