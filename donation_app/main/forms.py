import imp
from tokenize import String
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms_sqlalchemy.orm import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from donation_app.models import User, DonationItem, DonationPlace
from donation_app.extensions import bcrypt

class DonationPlaceForm(FlaskForm):
    title = StringField('Donation Place Name', validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField('Donation Place Address', validators=[DataRequired(), Length(min=3, max=120)])
    item_types = StringField('Types of Items Accepted', validators=[Length(min=3, max=120)])
    submit = SubmitField('Add New Donation Place')


# class GroceryItemForm(FlaskForm):
#     """Form for adding/updating a GroceryItem."""
#     name = StringField('Product Name',
#         validators=[DataRequired(), Length(min=3, max=80)])
#     price = FloatField('Product Price',
#         validators=[DataRequired()])
#     category = SelectField('Product Category', choices=ItemCategory.choices())
#     photo_url = StringField('Product Photo URL')
#     store = QuerySelectField('Store',
#         query_factory=lambda: GroceryStore.query, allow_blank=False)
#     submit = SubmitField('Add New Product')

# class BookForm(FlaskForm):
#     """Form to create a book."""
#     title = StringField('Book Title',
#         validators=[DataRequired(), Length(min=3, max=80)])
#     publish_date = DateField('Date Published')
#     author = QuerySelectField('Author',
#         query_factory=lambda: Author.query, allow_blank=False)
#     audience = SelectField('Audience', choices=Audience.choices())
#     genres = QuerySelectMultipleField('Genres',
#         query_factory=lambda: Genre.query)
#     submit = SubmitField('Submit')


# class AuthorForm(FlaskForm):
#     name = StringField('Author Name',
#         validators=[DataRequired(), Length(min=3, max=80)])
#     biography = TextAreaField('Author Biography')
#     # birthdate = DateField('Author Birthdate')
#     submit = SubmitField('Submit')


# class GenreForm(FlaskForm):
#     name = StringField('Genre Name',
#         validators=[DataRequired(), Length(min=3, max=80)])
#     submit = SubmitField('Submit')