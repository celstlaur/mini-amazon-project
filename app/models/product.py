from flask import current_app as app


class Product:
    def __init__(self, id, name, creator_id, category, product_description, price):
        self.id = id
        self.name = name
        self.creator_id = creator_id
        self.category = category
        self.product_description = product_description
        self.price = price

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

# can make a bunch more of these, easy to make...
    @staticmethod
    def get_all_less_than_equal_to_price(price):
        rows = app.db.execute('''
SELECT id, name, creator_id, category, product_description, price
FROM Products
WHERE price <= :price
''',
                              price=price)
        return [Product(*row) for row in rows]
