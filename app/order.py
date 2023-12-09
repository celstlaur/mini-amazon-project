from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.user import User
from .models.carts import Product
from .models.carts import Cart
from .models.orders import Order




from flask import Blueprint
bp = Blueprint('order', __name__)



@bp.route('/orders')
def orders():
    orders = Order.users_cart(current_user.id)
    return render_template('orders.html', title='Orders', orders=orders)
    cart_items = Product.users_cart(current_user.id)
    total_cost = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', title='Cart', current_user=current_user, cart_items=cart_items, total_cost=total_cost)

@bp.route('/place_order', methods=['POST'])
def place_order():
    user_id = current_user.id
    #ADD CHECK FOR SUFFICIENT FUNDS
    # Get the current user's cart items
    cart_items = Product.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Cannot place an empty order.', 'warning')
        return redirect(url_for('cart.cart'))

    # Create a new order and add items
    order = Order(user_id=current_user.id)
    db.session.add(order)

    for item in cart_items:
        order.add_item(item.product_id, item.quantity)

    # Clear the user's cart
    Product.clear_cart(current_user.id)

    db.session.commit()

    flash('Order placed successfully!', 'success')
    return redirect(url_for('order.orders'))
