from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_login import current_user
from datetime import date, datetime
from donation_app.models import ItemType, User, DonationPlace, DonationItem
from donation_app.main.forms import DonationPlaceForm

from donation_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

def decode_itemtype(array_of_items):
    str_array = []
    for item in array_of_items:
        for choice in ItemType.choices():
            if item == choice[0]:
                item_str = str(choice[1])
                print(item_str)
                str_array.append(item_str)
    return str_array

@main.route('/')
def homepage():
    return render_template('home.html')

@main.route('/donation_places')
def donation_places_index():
    all_places = DonationPlace.query.all()
    return render_template('donation_places.html', all_places=all_places)

@main.route('/view_donation_place/<donation_place_id>')
def donation_place_view(donation_place_id):
    place = DonationPlace.query.filter_by(id=donation_place_id).one()
    print(place.item_types)
    items = decode_itemtype(place.item_types)
    print(items)

    return render_template('view_donation_place.html', place=place, items=items)

@main.route('/new_donation_place', methods=['GET', 'POST'])
def donation_places_new():
    form = DonationPlaceForm()
    if form.validate_on_submit():
        # items = form.item_types.data
        # print(items)
        # item_types = items.split(", ")
        place = DonationPlace(
            title = form.title.data,
            address = form.address.data,
            item_types = form.item_types.data,
            description = form.description.data,
            date_added = datetime.now()
        )
        print(place.item_types)
        db.session.add(place)
        db.session.commit()
        return redirect(url_for('main.donation_place_view', donation_place_id=place.id))
    return render_template('create_donation_place.html', form=form)

@main.route('/profile/<username>')
@login_required
def profile(username):
    return render_template('profile.html')
