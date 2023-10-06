from flask import render_template, jsonify
from flask import redirect, url_for

from flask_login import current_user

from .models.cart import CartContents


from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    # Make sure user is logged in
    if not current_user.is_authenticated:
        return jsonify({}), 404

    # Get the current user's ID
    user_id = current_user.id

    items = CartContents.get_cart(user_id)

    # render the page by getting wishlist items
    return render_template('cart.html',
                      items=items,
                      quantity=quantity)



# add a second endpoint: wishlist_add(product_id)
#   see tutorial->endpoints->pt5
#   adds the product with the given id to this user's wishlist
@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    # Make sure user is logged in
    if not current_user.is_authenticated:
        return jsonify({}), 404
    
    user_id = current_user.id
    

    CartContents.add_to_cart(user_id, product_id)

    # If successful, redirect user to the newly updated wishlist
    return redirect(url_for('cart.cart'))