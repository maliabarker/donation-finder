from donation_app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """USER MODEL"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    shopping_list_items = db.relationship('GroceryItem', secondary='user_shopping_list')