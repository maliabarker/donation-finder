from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user
from datetime import date, datetime
from donation_app.models import User
# from donation_app.main.forms import 

from donation_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)