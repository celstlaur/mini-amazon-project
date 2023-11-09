from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime

from .models.product import Product
from .models.orderfact import OrderFact
from .models.inventory import Inventory
from .models.carts import Cart

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    products = Product.get_all()
    if current_user.is_authenticated:
        purchases = OrderFact.get_orders_given_buyer(current_user.id)
        return render_template('index.html', avail_products=products, 
                                            purchase_history=purchases, 
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id))
    else:
        return render_template('index.html', avail_products=products)

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
        cart = Cart.users_cart(current_user.id)
        return render_template('cart.html', cart=cart)
    else:
        return redirect(url_for('index.index'))
    