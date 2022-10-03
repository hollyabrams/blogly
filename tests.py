from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for user views"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        harry = User(first_name="Harry", last_name="Potter", image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/UX_Honeycomb.png/442px-UX_Honeycomb.png")
        db.session.add(harry)
        db.session.commit()

        self.user_id = harry.id
        

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_list_users(self):
        """Test /users route"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)


    def test_create_user(self):
        """Test create users route"""
        with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create User</h1>', html)


    def test_edit_user(self):
        """Test edit user route"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit User</h1>", html)

