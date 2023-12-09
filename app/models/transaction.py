from flask import current_app as app


class Transaction:
    def __init__(self, buyer_id, seller_id):
        self.buyer_id = buyer_id
        self.seller_id = seller_id

    def transactions(id):
        rows = app.db.execute('''
                            SELECT t1.buyer_id, t2.seller_id
                            FROM OrderFact AS t1, OrderContents AS t2
                            WHERE t1.id = t2.order_id
                            AND t1.buyer_id = :id''', id = id)
        return [Transaction(*row) for row in rows] if rows else None