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
    
    
class OrderHistory:
    def __init__(self, order_id, product_name, quantity, fulfill_status, timestamp, first, last, price_each):
        self.order_id = order_id
        self.product_name = product_name
        self.quantity = quantity
        self.fulfill_status = fulfill_status
        self.timestamp = timestamp
        self.first = first
        self.last = last
        self.price_each = price_each
        
    def get_seller_history(seller_id, limit, offset):
        rows = app.db.execute('''
select c.order_id, p.name, c.quantity, ful.fufillment_status, f.time_purchased, u.firstname, u.lastname, p.price 
FROM OrderContents c 
LEFT JOIN OrderFact f on c.order_id=f.id 
LEFT JOIN Products p on c.product_id=p.id 
LEFT JOIN Users u on u.id=f.buyer_id 
LEFT JOIN Fulfills ful on ful.order_id=c.order_id and ful.seller_id=c.seller_id 
WHERE c.seller_id= :seller_id
ORDER BY fufillment_status, time_purchased
LIMIT :limit OFFSET :offset ;  
                              ''',
                              seller_id=seller_id, limit=limit, offset=offset)
        return [OrderHistory(*row) for row in rows] if rows else None
    
    
    def get_seller_history_length(seller_id):
            rows = app.db.execute('''
    select *
    FROM OrderContents c 
    WHERE c.seller_id= :seller_id;  
                                ''',
                                seller_id=seller_id)
            return len(rows) if rows else 0