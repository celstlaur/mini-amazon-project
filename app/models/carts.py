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
   def get_all():
        rows = app.db.execute('''
        SELECT id, product_id, name, seller_id, quantity, price
        FROM Products
        ''')
        return [Product(*row) for row in rows]

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

   @staticmethod
   def remove_from_cart(user_id, product_id):
        Cart.cart_items = [[item] for item in Cart.cart_items if not (item['user_id'] == user_id and item['product'].id == product_id)]
        '''user_cart = Cart.users_cart(user_id)
        item_index_to_remove = None
        for i, item in enumerate(user_cart):
            if item.product_id == product_id:
                item_index_to_remove = i
                break
        if item_index_to_remove is not None:
            del user_cart[item_index_to_remove]
        return user_cart'''
        return Cart.cart_items

   @staticmethod
   def update_cart_quantity(user_id, product_id, new_quantity):
        try:
            rows = app.db.execute("""
                UPDATE Cart
                SET quantity = :new_quantity
                WHERE user_id = :user_id AND product_id = :product_id
            """, new_quantity=new_quantity, user_id=user_id, product_id=product_id)

            return True
        except Exception as e:
            print(str(e))
            return None

   def create_order(self):
        try:
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


class CartContents:
   def __init__(self, product_id, product_name, quantity, price):
       self.product_id = product_id
       self.product_name = product_name
       self.quantity = quantity
       self.price = price

   @staticmethod
   def get_cart(user_id):
        print("a")
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
    
   def calculate_total_products(cart):
       total_products = sum(item.quantity for item in cart)
       return total_products

   @staticmethod
   def decrease_quantity(user_id, product_id, quantity):
       app.db.execute('''
       UPDATE CartContents SET quantity=:quantity
       WHERE user_id=:user_id AND product_id=:product_id''',
       user_id=user_id, product_id=product_id, quantity=quantity-1)
       return

   @staticmethod
   def increase_quantity(user_id, product_id, quantity):
       app.db.execute('''
       UPDATE CartContents SET quantity=:quantity
       WHERE user_id=:user_id AND product_id=:product_id''',
       user_id=user_id, product_id=product_id, quantity=quantity+1)
       return
        
