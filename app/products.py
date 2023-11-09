from flask import render_template
from flask import jsonify
from flask_login import current_user
from flask import redirect, url_for
import datetime

from .models.product import Product

from flask import Blueprint, request
bp = Blueprint('products', __name__)


@bp.route('/products/page/<product>', methods = {"GET"})
def getprodpage(product):

    product = Product.get(product)

    # render the page by adding information to the index.html file
    return render_template('productpage.html',
                           product=product)

@bp.route('/products/findexpensive/', methods = {"GET"})
def find_most_expensive_products():

    k = request.args.get('k')
    # get most expensive available products for sale:
    expensive = Product.get_k_most_expensive(k)

    # render the page by adding information to the index.html file
    return render_template('productfilters.html',
                           filteredproducts=expensive)

@bp.route('/products/filtercategory/', methods = {"GET"})
def find_category():

    k = request.args.get('k')
    # get products for sale in category:
    filtcat = Product.get_by_category(k)

    # render the page by adding information to the index.html file
    return render_template('productfilters.html',
                           filteredproducts=filtcat)

@bp.route('/products/filterkeyword/', methods = {"GET"})
def find_keyword():

    k = request.args.get('k')
    # get products for sale in category:
    filtdesc = Product.get_by_desc(k)

    # render the page by adding information to the index.html file
    return render_template('productfilters.html',
                           filteredproducts=filtdesc)

