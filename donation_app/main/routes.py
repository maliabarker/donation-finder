from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_login import current_user
from datetime import date, datetime
from donation_app.models import ItemType, User, DonationPlace, DonationItem
from donation_app.main.forms import DonationPlaceForm, DonationItemForm
import os
from werkzeug.utils import secure_filename

from donation_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

def decode_itemtype(array_of_items):
    str_array = []
    for item in array_of_items:
        for choice in ItemType.choices():
            if item == choice[0]:
                item_str = str(choice[1])
                # print(item_str)
                str_array.append(item_str)
    return str_array

@main.route('/')
def homepage():
    return render_template('home.html')

###################################
###################################
###       Donation Places       ###
###################################
###################################

@main.route('/donation_places')
def donation_places_index():
    all_places = DonationPlace.query.all()
    return render_template('donation_places.html', all_places=all_places)

@main.route('/view_donation_place/<donation_place_id>')
def donation_place_view(donation_place_id):
    place = DonationPlace.query.filter_by(id=donation_place_id).one()
    items = decode_itemtype(place.item_types)
    return render_template('view_donation_place.html', place=place, items=items)

@main.route('/new_donation_place', methods=['GET', 'POST'])
def donation_places_new():
    form = DonationPlaceForm()
    if form.validate_on_submit():
        place = DonationPlace(
            title = form.title.data,
            address = form.address.data,
            item_types = form.item_types.data,
            description = form.description.data,
            date_added = datetime.now()
        )
        db.session.add(place)
        db.session.commit()
        return redirect(url_for('main.donation_place_view', donation_place_id=place.id))
    return render_template('create_donation_place.html', form=form)

###################################
###################################
###  Profiles & Donation Items  ###
###################################
###################################

@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)

@main.route('/items/<username>')
@login_required
def view_items(username):
    user = User.query.filter_by(username=username).one()
    items = DonationItem.query.filter_by(created_by_id=user.id).all()
    return render_template('items.html', user=user, user_items=items)

@main.route('/items/create', methods=['GET', 'POST'])
@login_required
def create_item():
    form = DonationItemForm()
    
    if form.validate_on_submit():
        merged_user = db.session.merge(current_user)

        image_dir = os.path.join(
            os.path.dirname(app.instance_path), 'donation_app/static/img'
        )

        img_file = form.photo.data
        # print(f'PROVIDED FILENAME {img_file.filename}')
        filename = secure_filename(img_file.filename)
        img_file.save(os.path.join(image_dir, filename))

        new_item = DonationItem(
            name = form.name.data,
            description = form.description.data,
            photo = img_file.filename,
            item_type = form.item_type.data,
            date_added = datetime.now(),
            created_by = merged_user
        )
        
        db.session.add(new_item)
        db.session.commit()
        flash('New Item Added')

        return redirect(url_for('main.view_items', username=current_user.username))
    return render_template('create_item.html', form=form)

@main.route('/items/<item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = DonationItem.query.filter_by(id=item_id).one()
    form = DonationItemForm(obj=item)

    if form.validate_on_submit():
        # if img_file != None and os.path.isfile(path) == False:
        if form.photo.data.filename:
            print('FILE NOT NULL, UPDATING FILENAME')
            image_dir = os.path.join(
                os.path.dirname(app.instance_path), 'donation_app/static/img'
            )
            img_file = form.photo.data
            # print(f'PROVIDED FILENAME {img_file.filename}')
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(image_dir, filename))
            item.photo = img_file.filename

        item.name = form.name.data
        item.description = form.description.data
        item.item_type = form.item_type.data

        item = db.session.merge(item)
        db.session.add(item)
        db.session.commit()

        flash(f'Updated {item.name}')
        return redirect(url_for('main.view_items', username=current_user.username))
    return render_template('edit_item.html', form=form, item=item)

@main.route('/items/<item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = DonationItem.query.filter_by(id=item_id).one()
    # print(item)
    item = db.session.merge(item)
    db.session.delete(item)
    db.session.commit()
    flash(f'Deleted {item.name}')
    # stretch challenge: try to add an undo button??
    return redirect(url_for('main.view_items', username=current_user.username))