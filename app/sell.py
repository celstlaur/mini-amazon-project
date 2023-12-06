from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.inventory import Inventory, InventoryList
from .models.ordercontents import OrderHistory, OrderViz
from . import DB

import math


from flask import Blueprint
bp = Blueprint('sell', __name__)

@bp.route('/sell', methods=['GET', 'POST'])
def sell():
    if current_user.is_authenticated:
        
        # determines table size
        page = request.args.get('page', 1, type=int)
        per_page = 10 
        offset = (page - 1) * per_page
        
        # finds order history, number of rows in order history
        order_history = OrderHistory.get_seller_history(current_user.id, per_page, offset)
        # can't call len on order_history variable, will be equal to 'per_page' every time
        history_length = OrderHistory.get_seller_history_length(current_user.id)
        
        # logic for front and back buttons
        if request.method == 'POST':
            if request.form['action'] == 'next':
                page += 1
            elif request.form['action'] == 'prev':
                page -= 1

            return redirect(url_for('sell.sell', page=page))
        
        return render_template('sell.html', 
                               seller_check=current_user.is_seller(current_user.id), 
                               history = order_history,
                               current_page = page,
                               history_length = history_length,
                               page_length = per_page)
    
    else:
        return redirect(url_for('index.index'))
    

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if current_user.is_authenticated:
        
        # determines table size
        page = request.args.get('page', 1, type=int)
        per_page = 5 
        offset = (page - 1) * per_page
        
        # finds inventory table
        inventory = Inventory.get_products_given_seller(current_user.id, per_page, offset)
        
        inventory_length = Inventory.get_inv_length(current_user.id)
        
        inventory_list_to_add = InventoryList.generate_lst(current_user.id)
        
        # logic for front and back buttons
        if request.method == 'POST':
            if request.form['action'] == 'next':
                page += 1
            elif request.form['action'] == 'prev':
                page -= 1

            return redirect(url_for('sell.inventory', page=page))
        
        return render_template('inventory.html', 
                               seller_check=current_user.is_seller(current_user.id), 
                               inventory = inventory,
                               current_page = page,
                               inventory_length = 9,
                               page_length = per_page,
                               lst = inventory_list_to_add)
    
    else:
        return redirect(url_for('index.index'))
    
@bp.route('/delete_from_inventory/<int:item_id>', methods=['POST', 'DELETE', 'GET'])
def delete_item(item_id):
    if current_user.is_authenticated:
       # Assuming CartItem has an 'id' attribute
        if Inventory.delete_inventory_item(pid=item_id, uid=current_user.id):
            flash('Item removed from cart.', 'success')
        else:
            flash('An error occurred', 'danger')
        return redirect(url_for('sell.inventory'))
    else:
        return redirect(url_for('index.index'))

@bp.route('/update_inventory_quant/<int:item_id>', methods=['POST', 'GET'])
def update_item(item_id):
    if current_user.is_authenticated:
       # Assuming CartItem has an 'id' attribute
        if Inventory.update_inventory_quantity(pid=item_id, uid=current_user.id, quant=request.form.get('quantity')):
            flash('Item Quantity Updated.', 'success')
        else:
            flash('An error occurred', 'danger')
        return redirect(url_for('sell.inventory'))
    else:
        return redirect(url_for('index.index'))
    
    
    
@bp.route('/update_fulfillment/<int:order_id>', methods=['POST', 'GET'])
def update_fulfillment(order_id):
    if current_user.is_authenticated:
       # Assuming CartItem has an 'id' attribute
        if OrderHistory.update_ordercontents_status(sid=current_user.id, oid=order_id):
            flash('Item Fulfillment Updated.', 'success')
        else:
            flash('An error occurred', 'danger')
        return redirect(url_for('sell.sell'))
    else:
        return redirect(url_for('index.index'))
    

@bp.route('/insert_new_item', methods=['POST', 'GET'])
def new_item():
    if current_user.is_authenticated:

        pid = request.form.get('product_name')
        quant = request.form.get('quantity')
        if Inventory.insert_new_item(user_id=current_user.id, pid=pid, quantity=quant):
            flash(f'Item Quantity Updated. {pid}', 'success')
        else:
            flash('An error occurred', 'danger')
        return redirect(url_for('sell.inventory'))
    else:
        return redirect(url_for('index.index'))
    
@bp.route('/viz')
def vis():
    if current_user.is_authenticated:
        # get original data in a  dictionary
        orders = OrderViz.fetch_data(current_user.id)
        
        # data for visualizations, init
        year_revenue = {}
        state_revenue = {}
        cat_revenue = {}
        prod_revenue = {}
        
        # get all rows in orignal data
        for o in orders:
            
            # different types of data to get from orders
            year_value = o['time'].year
            state = o['address'].split(' ')[-2]
            cat = o['category']
            prod = o['pname']
            
            # build out dictionaries for data vis
            if year_value not in year_revenue:
                year_revenue[year_value] = 0
            year_revenue[year_value] += float(o['price'])
            
            if state not in state_revenue:
                state_revenue[state] = 0
            state_revenue[state] += float(o['price'])
            
            if cat not in cat_revenue:
                cat_revenue[cat] = 0
            cat_revenue[cat] += float(o['price'])
            
            if prod not in prod_revenue:
                prod_revenue[prod] = 0
            prod_revenue[prod] += float(o['price'])
            
        # sort relavent dictionaries to improve output 
        sorted_year = {key: year_revenue[key] for key in sorted(year_revenue.keys())}
        sorted_states = {key: state_revenue[key] for key in sorted(state_revenue, key=lambda k: state_revenue[k], reverse=True)}
        sorted_prod = {key: prod_revenue[key] for key in sorted(prod_revenue, key=lambda k: prod_revenue[k], reverse=True)}
        
        # reduce number of slices in pie charts
        top_5 = dict(list(sorted_states.items())[:5])
        others_value = sum(list(sorted_states.values())[5:])
        result_dict = {**top_5, 'others': others_value}
        
        top_5_prod = dict(list(sorted_prod.items())[:5])
        others_value_prod = sum(list(sorted_prod.values())[5:])
        result_dict_prod = {**top_5_prod, 'others': others_value_prod}
        
        # round output to improve output
        for k, v in sorted_year.items():
            sorted_year[k] = round(v, 2)
        for k, v in result_dict.items():
            result_dict[k] = round(v, 2)
        for k, v in cat_revenue.items():
            cat_revenue[k] = round(v, 2)
        for k, v in result_dict_prod.items():
            result_dict_prod[k] = round(v, 2)
            
        return render_template('viz.html', seller_check=current_user.is_seller(current_user.id), 
                                           years = list(sorted_year.keys()), 
                                           years_val = list(sorted_year.values()), 
                                           states= list(result_dict.keys()), 
                                           states_val = list(result_dict.values()),
                                           cats = list(cat_revenue.keys()),
                                           cats_val = list(cat_revenue.values()),
                                           prods= list(result_dict_prod.keys()), 
                                           prods_val = list(result_dict_prod.values()))
    
    else:
        return redirect(url_for('index.index'))