from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from donation_app.models import User
from donation_app.auth.forms import SignUpForm, LoginForm

# Import app and db from events_app package so that we can run app
from donation_app.extensions import app, db, bcrypt

auth = Blueprint("auth", __name__)