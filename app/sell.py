from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.inventory import Inventory
from .models.ordercontents import OrderHistory
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
                               page_length = per_page)
    
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

        if Inventory.insert_new_item(product_name=request.form.get('product_name'), user_id=current_user.id, category=request.form.get('product_category'), product_description=request.form.get('product_description'), price=request.form.get('price'), quantity=request.form.get('quantity')):
            flash('Item Quantity Updated.', 'success')
        else:
            flash('An error occurred', 'danger')
        return redirect(url_for('sell.inventory'))
    else:
        return redirect(url_for('index.index'))