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
    def __init__(self, order_id, product_name, product_id, quantity, fulfill_status, timestamp, first, last, price_each, address):
        self.order_id = order_id
        self.product_name = product_name
        self.product_id = product_id
        self.quantity = quantity
        self.fulfill_status = fulfill_status
        self.timestamp = timestamp
        self.first = first
        self.last = last
        self.price_each = price_each
        self.address = address
        
    def get_seller_history(seller_id, limit, offset):
        rows = app.db.execute('''
select c.order_id, p.name, p.id, c.quantity, ful.fufillment_status, f.time_purchased, u.firstname, u.lastname, p.price, ua.address
FROM OrderContents c 
LEFT JOIN OrderFact f on c.order_id=f.id 
LEFT JOIN Products p on c.product_id=p.id 
LEFT JOIN Users u on u.id=f.buyer_id 
LEFT JOIN Fulfills ful on ful.order_id=c.order_id and ful.seller_id=c.seller_id 
LEFT JOIN UserAddress ua on ua.id = u.id
WHERE c.seller_id= :seller_id
ORDER BY fufillment_status, time_purchased
LIMIT :limit OFFSET :offset ;  
                              ''',
                              seller_id=seller_id, limit=limit, offset=offset)
        return [OrderHistory(*row) for row in rows] if rows else None


    def insert_user_purchase_history(self, user_id):
        try:
            # Insert order details into the user's purchase history
            app.db.execute('''
                INSERT INTO OrderHistory (order_id, product_name, product_id, quantity, fulfillment_status, timestamp, first, last, price_each, address)
                VALUES (:user_id, :order_id, :product_name, :product_id, :quantity, :fulfillment_status, :timestamp, :first, :last, :price_each, :address)
            ''', user_id=user_id, order_id=self.order_id, product_name=self.product_name, product_id=self.product_id,
                           quantity=self.quantity, fulfillment_status=self.fulfill_status, timestamp=self.timestamp,
                           first=self.first, last=self.last, price_each=self.price_each, address=self.address)
            return True
        except Exception as e:
            print(e)
            return False
    
    
    def get_seller_history_length(seller_id):
            rows = app.db.execute('''
    select *
    FROM OrderContents c 
    WHERE c.seller_id= :seller_id;  
                                ''',
                                seller_id=seller_id)
            return len(rows) if rows else 0
    
    @staticmethod
    def update_ordercontents_status(oid, sid):
        try:
            # Fetch the current fulfillment_status
            current_status = app.db.execute('''SELECT fufillment_status FROM Fulfills WHERE seller_id = :seller_id AND order_id = :order_id''', seller_id=sid, order_id=oid)
            
            # Toggle the fulfillment_status
            new_status = not current_status[0][0]

            # Update the fulfillment_status in the database
            app.db.execute('''UPDATE Fulfills SET fufillment_status = :new_status WHERE seller_id = :seller_id AND order_id = :order_id''', seller_id=sid, order_id=oid, new_status=new_status)
            print(1)
            return True
        except Exception as e:
            print(e)
            return False
