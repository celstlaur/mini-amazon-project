# app/models/orders.py
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Cart:
   def __init__(self, user_id, product_id, seller_id, quantity):
       self.user_id = user_id
       self.product_id = product_id
       self.seller_id = seller_id
       self.quantity = quantity

class Order:
    '''id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    
    product = db.relationship('Product', backref='order_items')'''
    #orders = []
    def __init__(self, user_id, product_id, seller_id, quantity):
        self.id = generate_unique_order_id() 
        self.user_id = user_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        #Order.orders.append(self)

    #def __repr__(self):
        #return f'<Order {self.id} - User {self.user_id} - Product {self.product_id}>'
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
    '''id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', backref='order_items')
    order = db.relationship('Order', backref='order_items')'''

    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity


    