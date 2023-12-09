from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime
import random

from .models.product import Product
from .models.orderfact import OrderFact
from .models.inventory import Inventory
from .models.carts import Cart, CartContents

from flask import Blueprint, request
bp = Blueprint('index', __name__)


@bp.route('/', methods = ['GET', 'POST'])
def index():

    # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    products = Product.get_byoffset(per_page, offset)
        

    products_all = Product.get_all()
    randproducts = [products_all[random.randint(0,len(products_all) - 1)], products_all[random.randint(0,len(products_all) - 1) ], products_all[random.randint(0,len(products_all) - 1)], products_all[random.randint(0,len(products_all) - 1)]]

    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('index.html',
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            avail_products = randproducts,
                                            seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id))
    else:
        return render_template('index.html', 
                               avail_products = randproducts)
    

#@bp.route('/seller')
#def seller():
#    if current_user.is_authenticated:
#        inventory = Inventory.get_products_given_seller(current_user.id)
#        return render_template('seller.html', inventory=inventory)
#    else:
#        return redirect(url_for('index.index'))
    
    
@bp.route('/cart')
def cart():
    if current_user.is_authenticated:
        cart = CartContents.get_cart(current_user.id)
        return render_template('cart.html', cart=cart)
    else:
        return redirect(url_for('index.index'))
    