from flask import current_app as app

class Cart:
    def __init__(self, user_id, product_id, seller_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        
    @staticmethod
    def users_cart(user_id):
       
        rows = app.db.execute('''
    SELECT *
    FROM CartContents
    WHERE user_id = :user_id
    ''',
                              user_id=user_id)
        return [Cart(*row) for row in rows] if rows else None