from flask import render_template, redirect, url_for, current_app, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

from .models.user import User
from .models.balance import Balance
from .models.orderfact import OrderFact
from . import DB


from flask import Blueprint
bp = Blueprint('account', __name__)

@bp.route('/account')
def account():
    if current_user.is_authenticated:
        balance = Balance.current_balance(current_user.id)
        full_address = User.get_address(current_user.id)
        address = full_address[0][0]
        purchases = OrderFact.get_orders_given_buyer(current_user.id)
    else:
        balance = None
        address = None
        purchases = None
    return render_template('account.html', title='Account', current_user=current_user, balance=balance, address=address, purchase_history=purchases,
                           seller_check=current_user.is_seller(current_user.id))


@bp.route('/public_profile')
def public_profile():
    num_purchases = User.num_purchases(current_user.id)
    num_sales = User.num_sales(current_user.id)
    return render_template('public_profile.html', title='Profile', current_user=current_user, num_sales=num_sales, num_purchases=num_purchases,
                           seller_check=current_user.is_seller(current_user.id))


@bp.route('/edit_name', methods=['POST'])
def edit_name():
    user_id = current_user.id
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    
    sqlstr = "UPDATE users SET firstname = :first_name, lastname = :last_name WHERE id = :user_id"
    db = DB(current_app)

    try:
        db.execute(sqlstr, first_name=first_name, last_name=last_name, user_id=user_id)
        flash('Your name has been updated!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('account.account'))

@bp.route('/edit_email', methods=['POST'])
def edit_email():
    user_id = current_user.id
    email = request.form.get('email')
    
    sqlstr = "UPDATE users SET email = :email WHERE id = :user_id"
    db = DB(current_app)

    try:
        db.execute(sqlstr, email=email, user_id=user_id)
        flash('Your email has been updated!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('account.account'))


@bp.route('/edit_address', methods=['POST'])
def edit_address():
    user_id = current_user.id
    address = request.form.get('address')
    
    sqlstr = "UPDATE UserAddress SET address = :address WHERE id = :user_id"
    db = DB(current_app)

    try:
        db.execute(sqlstr, address=address, user_id=user_id)
        flash('Your address has been updated!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('account.account'))

@bp.route('/change_password', methods=['POST'])
def change_password():
    user_id = current_user.id
    password = request.form.get('password')
    
    sqlstr = "UPDATE users SET password = :password WHERE id = :user_id"
    db = DB(current_app)

    try:
        db.execute(sqlstr, password=generate_password_hash(password), user_id=user_id)
        flash('Your password has been updated!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('account.account'))

@bp.route('/deposit', methods=['POST'])
def deposit():
    amount = request.form.get('amount', type=float)
    if amount <= 0:
        flash('You must deposit a positive amount.', 'danger')
        return redirect(url_for('account.account'))

    user_id = current_user.id
    new_balance = Balance.calculate_new_balance(user_id, amount)
    Balance.insert_new_balance(user_id, new_balance)
    
    flash('Deposit successful!', 'success')
    return redirect(url_for('account.account'))

@bp.route('/withdraw', methods=['POST'])
def withdraw():
    amount = request.form.get('amount', type=float)
    if amount <= 0:
        flash('You must withdraw a positive amount.', 'danger')
        return redirect(url_for('account.account'))

    user_id = current_user.id
    current_balance = Balance.current_balance(user_id)
    if current_balance < amount:
        flash('Insufficient funds.', 'danger')
        return redirect(url_for('account.account'))

    new_balance = Balance.calculate_new_balance(user_id, -amount)
    Balance.insert_new_balance(user_id, new_balance)

    flash('Withdrawal successful!', 'success')
    return redirect(url_for('account.account'))