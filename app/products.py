from flask import render_template
from flask import jsonify
from flask_login import current_user
from flask import redirect, url_for
import datetime

from .models.product import Product
from .models.orderfact import OrderFact
from .models.inventory import Inventory
from .models.seller import Seller

from flask import Blueprint, request
bp = Blueprint('products', __name__)


@bp.route('/cart/add/<int:product_id>/<int:seller_id>/<int:seller_quant>')
def add_to_cart(product_id, seller_id, seller_quant):
    if current_user.is_authenticated:

        # THIS NEEDS TO BE EDITED TO ACTUALLY WORK LOL

        user_id = current_user.id

        quantity = request.form["k"]

        if quantity > seller_quant:
            return jsonify({"Impossible to complete order"})

        return render_template('cart.html', title='Cart', current_user=current_user, cart_items=cart_items, total_cost=total_cost)

        #FeedbackItem.add_product_feedback(user_id, product_id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404

@bp.route('/products/page/<product>', methods = {"GET", "POST"})
def getprodpage(product):

    products = Product.get(product)

     # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 4
    offset = (page - 1) * per_page

    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('productpage.productpage', page = page))


    sellers = Inventory.get_sellers_given_product(product, per_page, offset)
    len_sellers = Inventory.get_len_sellers_given_prod(product)
    # render the page by adding information to the index.html file
    return render_template('productpage.html',
                           current_user=current_user,
                            current_page = page,
                            page_length = per_page,
                           product=products,
                           sellers = sellers,
                           len_sellers = len_sellers)

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
        
        return redirect(url_for('products.sort_asc', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtcat, 
                               current_user=current_user,
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            price = "asc")
    else:
        return render_template('buy.html', avail_products=filtcat,
                               current_user=current_user,
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

        return redirect(url_for('products.sort_desc', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=desc, 
                               current_user=current_user,
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            price = "desc")
    else:
        return render_template('buy.html', avail_products=desc,
                               current_user=current_user,
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

        return redirect(url_for('products.get_leq', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=lenleq,
                               current_user=current_user, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = lenq,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            category = k)
    else:
        return render_template('buy.html', avail_products=lenleq,
                               current_user=current_user,
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

        return redirect(url_for('products.get_geq', page = page))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=geq,
                               current_user=current_user, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = lengeq,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            category = k)
    else:
        return render_template('buy.html', avail_products=geq,
                               current_user=current_user,
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

        return redirect(url_for('products.find_category', page = page, k = k))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtcat,
                               current_user=current_user, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            category = k)
    else:
        return render_template('buy.html', avail_products=filtcat,
                               current_user=current_user,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               category = k)
    
@bp.route('/products/filtercategory/asc/', methods = {"GET", "POST"})
def find_category_asc():

    if not k:
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

        return redirect(url_for('products.find_category_asc', page = page, k = k))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtcat,
                               current_user=current_user, 
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
                               current_user=current_user,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               category = k,
                               price = "asc")



@bp.route('/products/filterkeyword/', methods = {"GET", "POST"})
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

        return redirect(url_for('products.find_keyword', page = page, k=k))

    # render the page by adding information to the index.html file
    if current_user.is_authenticated:
        purchases = OrderFact.get_paged_orders(current_user.id, page, per_page)
        return render_template('buy.html', avail_products=filtdesc,
                               current_user=current_user, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = len,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id),
                                            keyword = k)
    else:
        return render_template('buy.html', avail_products=filtdesc,
                               current_user=current_user,
                               current_page = page,
                               page_length = per_page,
                               total_avail = len,
                               keyword = k)
    

@bp.route('/product/edit_name/<int:product_id>', methods=['GET', 'POST'])
def edit_name(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id
        new_text = request.form["k"]

        #return render_template('submitfeedback.html')
        
        test = Product.edit_product_name(product_id, new_text)
        #print(test)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for("products.getprodpage", product = product_id))

    
    else:
        return jsonify({}), 404
    
@bp.route('/product/edit_desc/<int:product_id>', methods=['GET', 'POST'])
def edit_desc(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id
        new_text_desc = request.form["n"]

        #return render_template('submitfeedback.html')

        test = Product.edit_product_desc(product_id, new_text_desc)
        #print(test)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for("products.getprodpage", product = product_id))

    
    else:
        return jsonify({}), 404
    
@bp.route('/product/edit_cat/<int:product_id>', methods=['GET', 'POST'])
def edit_cat(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id
        new_text_cat = request.form["l"]

        #return render_template('submitfeedback.html')

        test = Product.edit_product_category(product_id, new_text_cat)
        #print(test)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for("products.getprodpage", product = product_id))

    
    else:
        return jsonify({}), 404
    
@bp.route('/product/edit_price/<int:product_id>', methods=['GET', 'POST'])
def edit_price(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id
        new_text_price = request.form["m"]



        #return render_template('submitfeedback.html')

        test = Product.edit_product_price(product_id, new_text_price)
        #print(test)


        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for("products.getprodpage", product = product_id))

    
    else:
        return jsonify({}), 404
    
@bp.route('/product/create/<int:creator_id>', methods=['GET', 'POST'])
def create(creator_id):
    if current_user.is_authenticated:

        creator_id = current_user.id
        price = request.form["price"]
        category = request.form["cat"]
        name = request.form["name"]
        new_desc = request.form['desc']



        #return render_template('submitfeedback.html')

        test, product_id = Product.create_new_product(name, creator_id, category, new_desc, price)
        #print(test)

        test2 = Seller.become_seller(current_user.id, current_user.email, current_user.email)


        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for("products.getprodpage", product = product_id))

    
    else:
        return jsonify({}), 404