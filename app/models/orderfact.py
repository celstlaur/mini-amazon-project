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
    
    def get_paged_orders(buyer_id, page, per_page):
        offset = (page - 1) * per_page

        # Query to count the total number of orders for pagination
        total_count_query = '''
        SELECT COUNT(*)
        FROM OrderFact
        WHERE buyer_id = :buyer_id
        '''
        total_count = app.db.execute(total_count_query, buyer_id=buyer_id)
        total_count = total_count[0][0] if total_count else 0

        # Calculating the total number of pages
        total_pages = (total_count + per_page - 1) // per_page

        # Query to fetch specific range of orders
        orders_query = '''
        SELECT id, buyer_id, total_price, fufillment_status, time_purchased
        FROM OrderFact
        WHERE buyer_id = :buyer_id
        ORDER BY time_purchased DESC
        LIMIT :limit OFFSET :offset
        '''
        orders = app.db.execute(orders_query, buyer_id=buyer_id, limit=per_page, offset=offset)

        # Convert rows to OrderFact objects if necessary
        # Assuming OrderFact is a class that can be instantiated with a row
        orders = [OrderFact(*row) for row in orders] if orders else []

        return orders, total_pages
    
