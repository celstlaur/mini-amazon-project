from flask import current_app as app


class Fulfills:
    def __init__(self, order_id, seller_id, status):
        self.order_id = order_id
        self.seller_id = seller_id
        self.status = status
        
# can always add more info here ... 
    @staticmethod
    def orders_not_completed(seller_id):
       
        rows = app.db.execute('''
    SELECT order_id
    FROM Fulfills
    WHERE seller_id = :seller_id and fufillment_status = False
    ''',
                              seller_id=seller_id)
        return [Fulfills(*row) for row in rows] if rows else None

    