from flask import current_app as app

class Inventory:
    def __init__(self, seller_id, product_id, quantity):
        self.seller_id = seller_id
        self.product_id = product_id
        self.quantity = quantity

# can build this out to join with products, get more info on products if needed...
    @staticmethod
    def get_products_given_seller(seller_id, available=False):
        if available:
            rows = app.db.execute('''
    SELECT product_id, quantity
    FROM HasInventory
    WHERE seller_id = :seller_id and quantity > 0
    ''',
                              seller_id=seller_id)
        else:
            rows = app.db.execute('''
    SELECT product_id, quantity
    FROM HasInventory
    WHERE seller_id = :seller_id
    ''',
                              seller_id=seller_id)
        return [Inventory(*row) for row in rows] if rows else None

# can build this out to join with Seller, get more info on sellers if needed...
    @staticmethod
    def get_sellers_given_product(product_id):
        rows = app.db.execute('''
    SELECT seller_id
    FROM HasInventory
    WHERE product_id = :product_id
    ''',
                              product_id=product_id)
        return [Inventory(*row) for row in rows] if rows else None