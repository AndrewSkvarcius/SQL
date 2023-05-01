"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://winaero.com/blog/wp-content/uploads/2017/12/User-icon-256-blue.png"


class User(db.Model):
    """Users."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text,
                     nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)


    @property
    def full_name(self):
        """Returns Full Name"""
        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect to database."""
  
    db.app = app
    db.init_app(app)