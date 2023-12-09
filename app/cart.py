from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import jsonify
from decimal import Decimal


from .models.user import User
from .models.product import Product
from .models.carts import Cart, CartContents
from .models.orders import Order, OrderItem
from .models.balance import Balance
from .models.ordercontents import OrderHistory



from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    if not current_user.is_authenticated:
        return jsonify({}), 404

    user_id = current_user.id
    cart_info = CartContents.get_cart(user_id)

    if cart_info:
        total_cost = CartContents.calculate_total_cost(cart_info)
        total_products = CartContents.calculate_total_products(cart_info)
    else:
        total_cost = 0
        total_products = 0


    return render_template('cart.html', cart=cart_info, total_cost=total_cost, total_products=total_products)


@bp.route('/quantity_minus/<product_id>/<quantity>', methods = ['GET', 'POST'])
def minus_item(product_id, quantity):
    user_id = current_user.id
    if int(quantity) > 1:
        CartContents.decrease_quantity(user_id, product_id, int(quantity))
    cart_items = CartContents.get_cart(user_id)
    #return render_template('cart.html', user_id=user_id, cart_items=cart_items)
    return redirect(url_for('cart.cart'))

@bp.route('/quantity_plus/<product_id>/<quantity>', methods = ['GET', 'POST'])
def plus_item(product_id, quantity):
    user_id = current_user.id
    CartContents.increase_quantity(user_id, product_id, int(quantity))
    cart_items = CartContents.get_cart(user_id)
    #return render_template('cart.cart', user_id=user_id, cart_items=cart_items)
    return redirect(url_for('cart.cart'))


@bp.route('/delete_item/<int:product_id>', methods=['POST', 'DELETE', 'Get'])
def delete_item(product_id):
    user_id = current_user.id
    CartContents.delete_from_cart(user_id, product_id)
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart.cart'))


@bp.route('/apply_discount', methods=['POST'])
def apply_discount():
    if not current_user.is_authenticated:
        return jsonify({}), 404

    user_id = current_user.id
    cart_info = CartContents.get_cart(user_id)

    if cart_info:
        total_cost = CartContents.calculate_total_cost(cart_info)
        total_products = CartContents.calculate_total_products(cart_info)
    else:
        total_cost = 0
        total_products = 0

    discount_code = request.form.get('discount_code')

    # Check the validity of the discount code
    #if discount_code:
    if (Cart.valid_code(discount_code) == 1):
        flash('Discount applied!', 'success')
        #total_cost = total_cost-100
        new_total_cost = CartContents.update_total_cost(total_cost, 100)
    else:
        flash('Invalid discount code', 'danger')
    # Redirect back to the cart page
    #return redirect(url_for('cart.cart'))
    return render_template('cart.html', cart=cart_info, total_cost=new_total_cost, total_products=total_products)


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
  if not current_user.is_authenticated:
      return jsonify({}), 404
  user_id = current_user.id
  cart.add_to_cart(user_id, product_id, quantity=1)
  return redirect(url_for('cart.cart'))


@bp.route('/place_order', methods=['POST'])
def place_order():
    if not current_user.is_authenticated:
        return jsonify({}), 404

    user_id = current_user.id
    cart_info = CartContents.get_cart(user_id)
    balance = Balance.current_balance(current_user.id)

    if cart_info:
        total_cost = CartContents.calculate_total_cost(cart_info)
        total_products = CartContents.calculate_total_products(cart_info)
    else:
        total_cost = 0
        total_products = 0

    if balance > total_cost:
        order_info = CartContents.get_cart(user_id)
        if cart_info:
            flash('Order placed successfully!', 'success')
            #OrderHistory.insert_user_purchase_history(user_id, order_info)
            for item in cart_info:
                CartContents.delete_from_cart(user_id, item.product_id)
            #balance = float(balance) - float(total_cost)
            '''amount = Decimal(total_cost)
            new_balance = Balance.calculate_new_balance(user_id, -amount)
            Balance.insert_new_balance(user_id, new_balance)'''
            return render_template('orders.html', orders=cart_info, total_cost=total_cost, total_products=total_products)
        else:
            flash('Failed to place the order. Please try again later.', 'danger')
            return redirect(url_for('cart.cart'))
    else:
        if balance < total_cost:
            flash('Insufficient funds. Please make a deposit and try again.', 'danger')
            return redirect(url_for('cart.cart'))
        else:
            flash('Some items unavailable. Please edit your cart and try again.', 'danger')
            return redirect(url_for('cart.cart'))
