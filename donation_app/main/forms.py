import imp
from tokenize import String
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, SelectMultipleField, MultipleFileField, widgets, FileField
from flask_wtf.file import FileAllowed
from wtforms_sqlalchemy.orm import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from donation_app.models import User, DonationItem, DonationPlace, ItemType
from donation_app.extensions import bcrypt

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class DonationPlaceForm(FlaskForm):
    title = StringField('Donation Place Name', validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField('Donation Place Address', validators=[DataRequired(), Length(min=3, max=120)])
    item_types = MultiCheckboxField('Types of Items Accepted', choices=ItemType.choices())
    description = StringField('Description or Notes', validators=[Length(min=3, max=120)])
    photos = MultipleFileField('Image File(s)', validators=[FileAllowed(['png'], 'PNG Images Only!')])
    submit = SubmitField('Add New Donation Place')

class DonationItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(min=3, max=80)])
    description = StringField('Item Description', validators=[Length(min=3, max=200)])
    # photo = StringField('Item Photo Path')
    photo = FileField('Item Image File', validators=[FileAllowed(['png'], 'PNG Image Only!')])
    item_type = SelectField('Item Type', choices=ItemType.choices())
    submit = SubmitField('Add New Donation Item')