from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models.product import Product
from .models.orderfact import OrderFact

from .models.user import User


from flask import Blueprint
bp = Blueprint('buy', __name__)

@bp.route('/buy', methods = ['GET', 'POST'])
def buy():

    # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    products = Product.get_byoffset(per_page, offset)
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))
        

    products_all = Product.get_all()
    if current_user.is_authenticated:
        purchases = OrderFact.get_orders_given_buyer(current_user.id)
        return render_template('buy.html', avail_products=products, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = products_all,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id))
    else:
        return render_template('buy.html', avail_products=products,
                               current_page = page,
                               page_length = per_page,
                               total_avail = products_all)
    return render_template('buy.html', title='Buy', current_user=current_user)
