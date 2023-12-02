from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.user import User
from .models.carts import Product
from .models.carts import Cart




from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
   cart_items = CartItem.users_cart(current_user.id)
   total_cost = sum(item.product.price * item.quantity for item in cart_items)
   return render_template('cart.html', title='Cart', current_user=current_user, cart_items=cart_items, total_cost=total_cost)






@bp.route('/delete_item/<int:item_id>', methods=['POST', 'DELETE'])
def delete_item(item_id):
   if request.method == 'DELETE':
       # Assuming CartItem has an 'id' attribute
       item = CartItem.query.get_or_404(item_id)
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
