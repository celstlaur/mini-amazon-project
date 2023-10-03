from flask import render_template, jsonify
from flask import redirect, url_for
    # url_for() is an important Flask feature that you should use as much as possible

from flask_login import current_user

from .models.wishlist import Wish

from humanize import naturaltime
import datetime
def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)


from flask import Blueprint
bp = Blueprint('wishlist', __name__)


@bp.route('/wishlist')
def wishlist():
    # Make sure user is logged in
    if not current_user.is_authenticated:
        return jsonify({}), 404

    # Get the current user's ID
    user_id = current_user.id

    items = Wish.get_all_by_uid(user_id)

    # render the page by getting wishlist items
    return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)



# add a second endpoint: wishlist_add(product_id)
#   see tutorial->endpoints->pt5
#   adds the product with the given id to this user's wishlist
@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    # Make sure user is logged in
    if not current_user.is_authenticated:
        return jsonify({}), 404
    
    user_id = current_user.id
    

    Wish.add_to_wishlist(user_id, product_id)

    # If successful, redirect user to the newly updated wishlist
    return redirect(url_for('wishlist.wishlist'))