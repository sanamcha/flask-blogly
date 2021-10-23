"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE ="http://www.pixelstalk.net/wp-content/uploads/2016/12/Color-Splash-Wallpaper-Full-HD.jpg"



class User(db.Model):
    """User Table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False, unique=True)
    last_name = db.Column(db.String, nullable=True)

    image_url = db.Column(db.Text, nullable=False, default = DEFAULT_IMAGE)


def connect_db(app):
    db.app = app
    db.init_app(app)