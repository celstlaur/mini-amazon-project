from flask import current_app as app

class Inventory:
    def __init__(self, seller_id, product_id, product_name, quantity):
        self.seller_id = seller_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity

# can build this out to join with products, get more info on products if needed...
    @staticmethod
    def get_products_given_seller(seller_id, limit, offset, available=False):
        if available:
            rows = app.db.execute('''
    SELECT h.seller_id, h.product_id, p.name, h.quantity
    FROM HasInventory h
    LEFT JOIN Products p on p.id = h.product_id
    WHERE seller_id = :seller_id and quantity > 0
    LIMIT :limit OFFSET :offset;
    ''',
                              seller_id=seller_id, limit=limit, offset=offset)
        else:
            rows = app.db.execute('''
    SELECT h.seller_id, h.product_id, p.name, h.quantity
    FROM HasInventory h
    LEFT JOIN Products p on p.id = h.product_id
    WHERE seller_id = :seller_id
    LIMIT :limit OFFSET :offset;
    ''',
                              seller_id=seller_id, limit=limit, offset=offset)
        return [Inventory(*row) for row in rows] if rows else None
    

    @staticmethod
    def get_inv_length(seller_id, available=False):
        if available:
            rows = app.db.execute('''
    SELECT h.seller_id, h.product_id, p.name, h.quantity
    FROM HasInventory h
    LEFT JOIN Products p on p.id = h.product_id
    WHERE seller_id = :seller_id and quantity > 0
    ''',
                              seller_id=seller_id)
        else:
            rows = app.db.execute('''
    SELECT h.seller_id, h.product_id, p.name, h.quantity
    FROM HasInventory h
    LEFT JOIN Products p on p.id = h.product_id
    WHERE seller_id = :seller_id
    ''',
                              seller_id=seller_id)
        return len(rows) if rows else 0

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
    
    @staticmethod
    def delete_inventory_item(pid, uid):
        try:
            app.db.execute('''DELETE FROM HasInventory WHERE seller_id = :uid AND product_id = :pid;''', uid=uid, pid=pid)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def update_inventory_quantity(pid, uid, quant):
        try:
            app.db.execute('''UPDATE HasInventory SET quantity = :quantity WHERE seller_id = :user_id and product_id =:item_id;''', user_id=uid, item_id=pid, quantity=quant)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def insert_new_item(product_name, user_id, category, product_description, price, quantity):
        try:
            new_item_id = app.db.execute("""INSERT INTO Products(name, creator_id, category, product_description, price) VALUES(:pname, :uid, :cat, :desc, :price) RETURNING id;""", pname=product_name, uid=user_id, cat=category, desc=product_description, price=price)
            app.db.execute("""INSERT INTO HasInventory(seller_id, product_id, quantity) VALUES(:sid, :pid, :quant);""", sid=user_id, pid=new_item_id[0][0], quant=quantity)
            return True
        except Exception as e:
            print(e)
            return False