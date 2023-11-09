from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.carts import Cart


from flask import Blueprint
bp = Blueprint('account', __name__)

@bp.route('/account')
def account():
    cart = Cart.users_cart(current_user.id)
    return render_template('account.html', title='Account', current_user=current_user, cart = cart)
