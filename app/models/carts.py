from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Product(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255), nullable=False)
   price = db.Column(db.Float, nullable=False)
   cart_items = db.relationship('Cart', backref='product', lazy=True)


class Cart:
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, nullable=False)
   product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
   seller_id = db.Column(db.Integer, nullable=False)
   quantity = db.Column(db.Integer, nullable=False)
  
   product = db.relationship('Product', backref='cart_items')


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
   def add_to_cart(user_id, product_id, quantity):
       existing_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()


       if existing_item:
           # Update quantity if the item is already in the cart
           existing_item.quantity += quantity
       else:
           # Add a new item to the cart
           new_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
           db.session.add(new_item)


       db.session.commit()
