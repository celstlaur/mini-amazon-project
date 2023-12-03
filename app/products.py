from flask import render_template
from flask import jsonify
from flask_login import current_user
from flask import redirect, url_for
import datetime

from .models.product import Product
from .models.orderfact import OrderFact

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

    # render the page by adding information to the index.html file
    return render_template('productfilters.html',
                           filteredproducts=expensive)

@bp.route('/products/asc/', methods = {"GET", "POST"})
def sort_asc():

        # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    filtcat = Product.get_asc(per_page, offset)

    len = Product.get_len_prods()
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtcat, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            price = "asc")
    else:
        return render_template('buy.html', avail_products=filtcat,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               price = "asc")
    
@bp.route('/products/desc/', methods = {"GET", "POST"})
def sort_desc():

        # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    desc = Product.get_desc(per_page, offset)

    len = Product.get_len_prods()
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=desc, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            price = "desc")
    else:
        return render_template('buy.html', avail_products=desc,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               price = "desc")
    
@bp.route('/products/max/', methods = {"GET", "POST"})
def get_leq():

    k = request.args.get('k')
    # get products for sale in category:

        # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    lenleq = Product.get_all_less_than_equal_to_price(k, per_page, offset)

    lenq = Product.get_len_leq(k)
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=lenleq, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = lenq,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            category = k)
    else:
        return render_template('buy.html', avail_products=lenleq,
                               current_page = page,
                               page_length = per_page,
                               total_avail = lenq,
                               category = k)
    
@bp.route('/products/min/', methods = {"GET", "POST"})
def get_geq():

    k = request.args.get('k')
    # get products for sale in category:

        # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    geq = Product.get_all_greater_than_price(k, per_page, offset)

    lengeq = Product.get_len_geq(k)
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=geq, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = lengeq,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            category = k)
    else:
        return render_template('buy.html', avail_products=geq,
                               current_page = page,
                               page_length = per_page,
                               total_avail = lengeq,
                               category = k)


@bp.route('/products/filtercategory/', methods = {"GET", "POST"})
def find_category():

    k = request.args.get('k')
    # get products for sale in category:

        # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    filtcat = Product.get_by_category(k, per_page, offset)

    len = Product.getbycat_length(k)
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtcat, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            category = k)
    else:
        return render_template('buy.html', avail_products=filtcat,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               category = k)
    
@bp.route('/products/filtercategory/asc/', methods = {"GET", "POST"})
def find_category_asc():

    k = request.args.get('k')
    # get products for sale in category:

        # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    filtcat = Product.get_by_category_asc(k, per_page, offset)

    len = Product.getbycat_length(k)
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtcat, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            category = k,
                                            price = "asc")
    else:
        return render_template('buy.html', avail_products=filtcat,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               category = k,
                               price = "asc")


@bp.route('/products/filterkeyword/', methods = {"GET"})
def find_keyword():

    k = request.args.get('k')
    # get products for sale in category:

            # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    filtdesc = Product.get_by_desc(k, per_page, offset)

    len = Product.getbydesc_length(k)
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('buy.buy', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtdesc, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            keyword = k)
    else:
        return render_template('buy.html', avail_products=filtdesc,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               keyword = k)


