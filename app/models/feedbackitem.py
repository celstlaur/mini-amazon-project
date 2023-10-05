from flask import current_app as app

class FeedbackItem:
    def __init__(self, review, timestamp):
        self.review = review
        self.timestamp = timestamp
    
    @staticmethod
    def get_all(user_id):
        rows = app.db.execute('''
                            (SELECT review, time_reviewed_seller AS time_reviewed
                            FROM ReviewedSeller
                            WHERE user_id = :user_id)
                            UNION
                            (SELECT review, time_reviewed_product AS time_reviewed
                            FROM ReviewedProduct
                            WHERE user_id = :user_id)
                            ORDER BY time_reviewed DESC LIMIT 5''', user_id = user_id)
        
        return [FeedbackItem(*row) for row in rows] if rows else None