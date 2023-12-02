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
    
@bp.route('/edit_inventory_quantity/<int:item_id>', methods=['POST', 'GET'])
def edit_quant(item_id):
    user_id = current_user.id
    quantity = request.form.get('quantity')
    
    sqlstr = "UPDATE HasInventory SET quantity = :quantity WHERE seller_id = :user_id and product_id =:item_id"
    db = DB(current_app)

    try:
        db.execute(sqlstr, user_id=current_user.id, item_id=item_id, quantity=quantity)
        flash('The quantity has been updated!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('sell.inventory'))