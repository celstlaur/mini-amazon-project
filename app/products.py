from flask import render_template
from flask import jsonify
from flask_login import current_user
from flask import redirect, url_for
import datetime

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products/findexpensive/<int:k>')
def find_most_expensive_products(k):

    # get most expensive available products for sale:
    filteredproducts = Product.get_k_most_expensive(k)

    # render the page by adding information to the index.html file
    return render_template('productfilters.html',
                           filteredproducts=filteredproducts)

