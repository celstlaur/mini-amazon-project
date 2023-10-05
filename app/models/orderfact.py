from flask import current_app as app


class OrderFact:
    def __init__(self, id, buyer_id, total_price, status, timestamp):
        self.id = id
        self.buyer_id = buyer_id
        self.total_price = total_price
        self.status = status
        self.timestamp = timestamp

    def get_order(id):
        rows = app.db.execute('''
SELECT id, buyer_id, total_price, fufillment_status, time_purchased
FROM OrderFact
WHERE id = :id
''',
                              id=id)
        return OrderFact(*(rows[0])) if rows is not None else None
    
    def get_orders_given_buyer(buyer_id):
        rows = app.db.execute('''
SELECT id, buyer_id, total_price, fufillment_status, time_purchased
FROM OrderFact
WHERE buyer_id = :buyer_id
''',
                              buyer_id=buyer_id)
        return [OrderFact(*row) for row in rows] if rows else None
    