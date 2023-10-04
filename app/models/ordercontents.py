from flask import current_app as app


class OrderContents:
    def __init__(self, order_id, product_id, seller_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity

    def get(order_id):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_id, quantity
FROM OrderContents
WHERE order_id = :order_id
''',
                              order_id=order_id)
        return [OrderContents(*row) for row in rows] if rows else None