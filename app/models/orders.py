# app/models/orders.py
from flask import current_app as app
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#db = SQLAlchemy()

class Cart:
   def __init__(self, user_id, product_id, seller_id, quantity):
       self.user_id = user_id
       self.product_id = product_id
       self.seller_id = seller_id
       self.quantity = quantity

class Order:
    def __init__(self, user_id, product_id, seller_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity

    @staticmethod
    def users_cart(user_id):
        rows = app.db.execute('''
    SELECT user_id, product_id, seller_id, quantity
    FROM CartContents
    WHERE user_id = :user_id
    ''',
                             user_id=user_id)
        return [Cart(*row) for row in rows] if rows else None
    
    @staticmethod
    def get_all_by_user_id(user_id):
        return [order for order in Order.orders if order.user_id == user_id]
        #return Order.query.filter_by(user_id=user_id).order_by(Order.time_placed.desc()).all()

class OrderItem:
    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity