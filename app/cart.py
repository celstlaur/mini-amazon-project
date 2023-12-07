from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.user import User
from .models.carts import Product
from .models.carts import Cart
from .models.orders import Order, OrderItem




from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
   cart_items = Product.users_cart(current_user.id)
   total_cost = sum(item.product.price * item.quantity for item in cart_items)
   return render_template('cart.html', title='Cart', current_user=current_user, cart_items=cart_items, total_cost=total_cost)






@bp.route('/delete_item/<int:product_id>', methods=['POST', 'DELETE'])
def delete_item(product_id):
   if request.method == 'DELETE':
       item = Product.query.get_or_404(product_id)
       db.session.delete(item)
       db.session.commit()
       flash('Item removed from cart.', 'success')
       return redirect(url_for('cart.cart'))




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

    if request.method == 'POST':
        user_id = current_user.id
        cart_items = Cart.users_cart(current_user.id)

        if not cart_items:
            flash('No items in the cart. Cannot place an order with an empty cart.', 'warning')
            return redirect(url_for('cart.cart'))

        # Assuming cart_items[0] contains the necessary information
        product_id = cart_items[0].product_id
        seller_id = cart_items[0].seller_id
        quantity = cart_items[0].quantity

        # Create Cart instance with the necessary arguments
        cart = Cart(user_id=user_id, product_id=product_id, seller_id=seller_id, quantity=quantity)
        order = Cart.create_order

        if order:
            flash('Order placed successfully!', 'success')
            #return redirect(url_for('order.orders', order_id=Order.id))
            return redirect(url_for('order.orders', order_id=order))
        else:
            flash('Failed to place the order. Please try again later.', 'danger')
            return redirect(url_for('cart.cart'))
    else:
        # Handle GET request (if needed)
        return redirect(url_for('cart.cart'))
