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

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT user_id, product_id, seller_id, quantity
FROM CartContents
WHERE user_id = :user_id
ORDER BY quantity DESC
''',
                              uid=uid)
        return [Wish(*row) for row in rows]

    @staticmethod
    def add_to_cart(uid, pid):
        try:
            current_time = datetime.datetime.now()
            rows = app.db.execute("""
INSERT INTO CartContents(user_id, product_id, seller_id, quantity)
VALUES(:user_id, :product_id, :seller_id, :time_added)
RETURNING id
""",
                                  uid=uid,
                                  pid=pid,
                                  time_added=current_time)
            id = rows[0][0]
            return Cart.get(id)
        except Exception as e:
            print(str(e))
            return None