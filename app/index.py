from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.orderfact import OrderFact

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all_less_than_equal_to_price(100000000)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = OrderFact.get_orders_given_buyer(current_user.id)
        return render_template('index.html', avail_products=products, purchase_history=purchases)
    else:
        return render_template('index.html', avail_products=products)