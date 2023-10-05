from flask import current_app as app

class CartContents:
    def __init__(self, id, product_id, seller_id, quantity):
        self.id = id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity

    def get_card(id):
        rows = app.db.execute(
            """
SELECT id, product_id, seller_id, quantity
FROM CartContents
WHERE id = :id
            """, id=id)
        return [CartContents(*row) for row in rows] if rows else None