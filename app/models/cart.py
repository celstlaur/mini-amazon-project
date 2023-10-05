from flask import current_app as app

class CartContents:
    def __init__(self, user_id, product_id, seller_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity

    def get_cart(id):
        rows = app.db.execute(
            """
SELECT user_id, product_id, seller_id, quantity
FROM CartContents
WHERE user_id = :user_id
            """, user_id=user_id)
        return [CartContents(*row) for row in rows] if rows else None