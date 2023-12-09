from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import jsonify


from .models.user import User
from .models.carts import Product
from .models.carts import CartContents
from .models.orders import Order, OrderContents
from .models.balance import Balance




from flask import Blueprint
bp = Blueprint('order', __name__)

@bp.route('/orders/<sid>/<purchase_id>', methods=['GET','POST'])
def orders(sid, purchase_id):
    if request.method == 'POST':
        if request.form['action'] == 'fulfill':
            OrderContents.item_fulfilled(request.form['id'])
    orders = OrderContents.get_by_seller_id(sid, purchase_id)
    return render_template("orders.html", orders = orders, purchase_id = purchase_id)




'''@bp.route('/orders')
def orders():
    orders = Order.users_cart(current_user.id)
    return render_template('orders.html', title='Orders', orders=orders)
    cart_items = Product.users_cart(current_user.id)
    total_cost = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', title='Cart', current_user=current_user, cart_items=cart_items, total_cost=total_cost)
'''
@bp.route('/place_order/<int:product_id>', methods=['POST'])
def place_order():
    if not current_user.is_authenticated:
        return jsonify({}), 404

    user_id = current_user.id
    product_id = product_id
    cart_info = CartContents.get_cart(user_id)
    balance = Balance.current_balance(current_user.id)

    if cart_info:
        total_cost = CartContents.calculate_total_cost(cart_info)
        total_products = CartContents.calculate_total_products(cart_info)
    else:
        total_cost = 0
        total_products = 0

    if balance > total_cost:
        if request.method == 'POST':
            user_id = current_user.id
            cart_info = CartContents.get_cart(user_id)

        if cart_info:
            flash('Order placed successfully!', 'success')
            for item in cart_info:
                CartContents.delete_from_cart(user_id, product_id)
            return render_template('orders.html', cart=cart_info, total_cost=total_cost, total_products=total_products)
        else:
            flash('Failed to place the order. Please try again later.', 'danger')
            return redirect(url_for('cart.cart'))
    else:
        flash('Insufficient funds. Please make a deposit and try again.', 'danger')
        return redirect(url_for('cart.cart'))
