from flask import current_app as app
from flask_login import current_user
from .inventory import Inventory


class Product:
   def __init__(self, user_id, product_id, product_name, seller_id, quantity, price):
       self.id = id
       self.user_id = user_id
       self.product_id = product_id
       self.product_name = product_name
       self.seller_id = seller_id
       self.quantity = quantity
       self.price = price


class Order:
   def __init__(self, user_id, product_id, seller_id, quantity):
       self.user_id = user_id
       self.product_id = product_id
       self.seller_id = seller_id
       self.quantity = quantity



class Cart:
   def __init__(self, user_id, product_id, seller_id, quantity, discount_code):
       self.user_id = user_id
       self.product_id = product_id
       self.seller_id = seller_id
       self.quantity = quantity
       self.discount_code = discount_code

   @staticmethod
   def valid_code(discount_code):
        if (discount_code == "100off"):
            return 1
        else:
            return 0


   @staticmethod
   def add_to_cart(user_id, product_id, quantity, seller_id):
        try:
            rows = app.db.execute("""
INSERT INTO CartContents(user_id, product_id, seller_id, quantity)
VALUES(:user_id, :product_id, :seller_id, :quantity)
""",
                                  user_id=user_id,
                                  product_id=product_id,
                                  seller_id = seller_id,
                                  quantity = quantity)
            return True
        except Exception as e:
            print(str(e))
            return None



class CartContents:
   def __init__(self, product_id, product_name, quantity, price):
       self.product_id = product_id
       self.product_name = product_name
       self.quantity = quantity
       self.price = price

   @staticmethod
   def get_cart(user_id):
        rows = app.db.execute('''
            SELECT c.product_id, p.name as product_name, c.quantity, p.price
            FROM CartContents c
            LEFT JOIN Products p ON p.id = c.product_id
            WHERE c.user_id = :user_id
        ''', user_id=user_id)
        
        return [CartContents(*row) for row in rows] if rows else None


   def calculate_total_cost(cart):
       total_cost = sum(item.price * item.quantity for item in cart)
       return total_cost

   def update_total_cost(total_cost, discount):
       new_total_cost = total_cost - discount
       return new_total_cost
    
   def calculate_total_products(cart):
       total_products = sum(item.quantity for item in cart)
       return total_products

   @staticmethod
   def increase_quantity(user_id, product_id, quantity):
       app.db.execute('''
       UPDATE CartContents SET quantity=:quantity
       WHERE user_id=:user_id AND product_id=:product_id''',
       user_id=user_id, product_id=product_id, quantity=quantity+1)
       return

   @staticmethod
   def decrease_quantity(user_id, product_id, quantity):
       app.db.execute('''
       UPDATE CartContents SET quantity=:quantity
       WHERE user_id=:user_id AND product_id=:product_id''',
       user_id=user_id, product_id=product_id, quantity=quantity-1)
       return

   @staticmethod
   def delete_from_cart(user_id, product_id):
        app.db.execute('''
            DELETE FROM CartContents
            WHERE user_id = :user_id AND product_id = :product_id
        ''', user_id=user_id, product_id=product_id)
        return
