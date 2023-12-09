from flask import current_app as app
from datetime import datetime


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
    FROM Order
    WHERE user_id = :user_id
    ''',
                             user_id=user_id)
        return [Order(*row) for row in rows] if rows else None
    
    @staticmethod
    def get_all_by_user_id(user_id):
        return [order for order in Order.orders if order.user_id == user_id]
        #return Order.query.filter_by(user_id=user_id).order_by(Order.time_placed.desc()).all()

class OrderItem:
    def __init__(self, order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity



class OrderContents:
    def __init__(self, id, purchase_id, seller_id, seller_name, product_id, product_name, price_at_placement, qty,
                 fulfillment_status):
        self.id = id
        self.purchase_id = purchase_id
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.product_id = product_id
        self.product_name = product_name
        self.price_at_placement = price_at_placement
        self.qty = qty
        self.fulfillment_status = fulfillment_status

    @staticmethod
    def get_all_related_oder_by_purchase_id(purchase_id):
        rows = app.db.execute('''
                                SELECT orders.id, orders.purchase_id,orders.seller_id, users.firstname || ' '|| users.lastname as seller_name, 
                                orders.product_id, products.name as product_name, orders.price_at_placement, orders.qty, orders.fulfillment_status
                                FROM orders 
                                join products  on orders.product_id = products.id 
                                join users on orders.seller_id = users.id
                                WHERE purchase_id = :purchase_id
                            ''', purchase_id=purchase_id)
        return [Order(*row) for row in rows]

    def get_by_product_id_and_buyer_id(product_id, buyer_id):
        rows = app.db.execute('''
                                SELECT Orders.id, purchase_id, seller_id, 'seller_name',product_id,'product_name', price_at_placement, qty, fulfillment_status
                                FROM Orders, Purchases
                                WHERE product_id = :product_id 
                                AND buyer_id = :buyer_id 
                                AND Orders.purchase_id = Purchases.id
                            ''', product_id=product_id, buyer_id=buyer_id)
        return [Order(*row) for row in rows]

    def get_by_seller_id(seller_id, purchase_id):
        rows = app.db.execute('''
                                SELECT orders.id, orders.purchase_id,orders.seller_id, users.firstname || ' '|| users.lastname as seller_name, 
                                orders.product_id, products.name as product_name, orders.price_at_placement, orders.qty, orders.fulfillment_status
                                FROM orders
                                join products  on orders.product_id = products.id 
                                join users on orders.seller_id = users.id
                                WHERE orders.seller_id = :seller_id
                                AND orders.purchase_id = :purchase_id
                            ''', seller_id=seller_id,
                              purchase_id=purchase_id)
        return [Order(*row) for row in rows]

    def get_by_id(id):
        rows = app.db.execute('''
                                SELECT orders.id, orders.purchase_id,orders.seller_id, users.firstname || ' '|| users.lastname as seller_name, 
                                orders.product_id, products.name as product_name, orders.price_at_placement, orders.qty, orders.fulfillment_status
                                FROM orders
                                join products  on orders.product_id = products.id 
                                join users on orders.seller_id = users.id
                                WHERE orders.id = :id
                            ''', id=id)
        return [Order(*row) for row in rows]

    @staticmethod
    def item_fulfilled(id):
        item_status = app.db.execute('''
            SELECT fulfillment_status
            FROM Orders
            WHERE Orders.id = :id
        ''',
                                     id=id)
        if item_status[0][0] == False:
            rows = app.db.execute('''
                UPDATE Orders
                SET fulfillment_status = TRUE, fulfillment_time = CURRENT_TIMESTAMP
                WHERE Orders.id = :id
            ''',
                                  id=id)
            return True
        else:
            return False

    @staticmethod
    def isUserOrderedFromSeller(user_id: int, seller_id: int):
        rows = app.db.execute('''
            SELECT *
            FROM Orders join Purchases on Purchases.id = Orders.purchase_id
            WHERE buyer_id = :buyer_id AND seller_id = :seller_id
        ''',
                              buyer_id=user_id, seller_id=seller_id)

        return False if rows is None or len(rows) == 0 else True

    @staticmethod
    def purchased_category(user_id: int):
        rows = app.db.execute('''
                            SELECT Distinct (c.name), count(c.name)
                            from orders
                                     join purchases p on orders.purchase_id = p.id
                                     join products p2 on orders.product_id = p2.id
                                     join categories c on p2.cid = c.id
                            where buyer_id = :user_id
                            group by c.name
                            order by count DESC
        ''',
                              user_id=user_id)

        return rows

