from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


class Product:
   '''id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255), nullable=False)
   price = db.Column(db.Float, nullable=False)
   cart_items = db.relationship('Cart', backref='product', lazy=True)'''
   def __init__(self, user_id, product_id, product_name, seller_id, quantity, price):
       self.user_id = user_id
       self.product_id = product_id
       self.product_name = product_name
       self.seller_id = seller_id
       self.quantity = quantity
       self.price = price


class Order:
   '''id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255), nullable=False)
   price = db.Column(db.Float, nullable=False)
   cart_items = db.relationship('Cart', backref='product', lazy=True)'''
   def __init__(self, user_id, product_id, seller_id, quantity):
       self.user_id = user_id
       self.product_id = product_id
       self.seller_id = seller_id
       self.quantity = quantity



class Cart:
   '''id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, nullable=False)
   product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
   seller_id = db.Column(db.Integer, nullable=False)
   quantity = db.Column(db.Integer, nullable=False)
  
   product = db.relationship('Product', backref='cart_items')'''


   def __init__(self, user_id, product_id, seller_id, quantity):
       self.user_id = user_id
       self.product_id = product_id
       self.seller_id = seller_id
       self.quantity = quantity
      
   
   def create_order(self):
        try:
            '''id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, nullable=False)
            product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
            seller_id = db.Column(db.Integer, nullable=False)
            quantity = db.Column(db.Integer, nullable=False)'''

            current_time = datetime.datetime.now()
            #order = Order(user_id=self.user_id, time_created=current_time)
            order = Order(user_id=self.user_id, product_id=self.product_id, seller_id=self.seller_id, quantity=self.quantity, time_created=current_time)
            db.session.add(order)
            db.session.commit()

            # Move cart items to order items
            for item in self.cart_items:
                order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
                db.session.add(order_item)
                db.session.commit()

            # Clear the cart after creating the order
            #self.cart_items = []
            #db.session.commit()

            return order
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return None
   
   @staticmethod
   def users_cart(user_id):
     
       rows = app.db.execute('''
   SELECT user_id, product_id, seller_id, quantity
   FROM CartContents
   WHERE user_id = :user_id
   ''',
                             user_id=user_id)
       return [Cart(*row) for row in rows] if rows else None


   def get_cart(user_id):
       rows = app.db.execute("""
SELECT user_id, product_id, seller_id, quantity
FROM CartContents
WHERE user_id = :user_id
            """, user_id=user_id)
       return CartContents(*(rows[0])) if rows else None


   @staticmethod
   def add_to_cart(user_id, product_id, quantity):
        try:
            current_time = datetime.datetime.now()
            rows = app.db.execute("""
INSERT INTO CartContents(user_id, product_id, seller_id, quantity)
VALUES(:user_id, :product_id, :seller_id, :time_added)
RETURNING id
""",
                                  user_id=user_id,
                                  product_id=product_id,
                                  time_added=current_time)
            id = rows[0][0]
            return Cart.get(user_id)
        except Exception as e:
            print(str(e))
            return None