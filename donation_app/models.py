from donation_app import db
from flask_login import UserMixin
from sqlalchemy_utils import URLType
import enum
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import ForeignKey, PickleType


class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)


class ItemType(FormEnum):
    CLOTHING =        'Clothing'
    FURNITURE =       'Furniture'
    ELECTRONICS =     'Electronics'
    BOOKS =           'Books'
    HOME_AND_GARDEN = 'Home and Garden'
    TOYS =            'Toys'
    COLLECTABLES =    'Collectables'
    MISC =            'Miscellaneous'


class DonationPlace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(120))
    item_types = db.Column(MutableList.as_mutable(PickleType),
                                    default=[])
    items = db.relationship('DonationItem', secondary='donation_place_item_list')
    # adds items to donation place from user item list, but cannot add items from donation place
    date_added = db.Column(db.Date)
    favorited_by = db.relationship('User', secondary='user_place')
    ### STRETCH: add pictures to donation place and show slideshows on site (like yelp)


class DonationItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    photo = db.Column(URLType)
    item_type = db.Column(db.Enum(ItemType), default=ItemType.MISC)
    donation_place = db.relationship('DonationPlace', secondary='donation_place_item_list', back_populates='items')
    date_added = db.Column(db.Date)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')


class User(UserMixin, db.Model):
    """USER MODEL"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    favorite_places = db.relationship('DonationPlace', secondary='user_place', back_populates='favorited_by')


favorite_donation_places_table = db.Table('user_place',
    db.Column('place_id', db.Integer, db.ForeignKey('donation_place.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

donation_place_items_list = db.Table('donation_place_item_list',
    db.Column('place_id', db.Integer, db.ForeignKey('donation_place.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('donation_item.id'))
)