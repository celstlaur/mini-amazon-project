from flask import current_app as app

class FeedbackItem:
    def __init__(self, reviewed, review, timestamp):
        self.reviewed = reviewed
        self.review = review
        self.timestamp = timestamp
    
    #@staticmethod
    #def get_all(user_id):
        #rows = app.db.execute('''
                            #(SELECT review, time_reviewed_seller AS time_reviewed
                            #FROM ReviewedSeller
                            #WHERE user_id = :user_id)
                            #UNION
                            #(SELECT review, time_reviewed_product AS time_reviewed
                            #FROM ReviewedProduct
                            #WHERE user_id = :user_id)
                            #ORDER BY time_reviewed DESC LIMIT 5''', user_id = user_id)
        
        #return [FeedbackItem(*row) for row in rows] if rows else None

    @staticmethod
    def get_all(user_id):
        rows = app.db.execute('''
                            (SELECT names.firstname AS reviewed, reviews.review, time_reviewed_seller AS time_reviewed
                            FROM ReviewedSeller AS reviews, Users AS names
                            WHERE reviews.user_id = :user_id
                            AND reviews.seller_id = names.id)
                            UNION
                            (SELECT descriptions.name AS reviewed, reviews.review, time_reviewed_product AS time_reviewed
                            FROM ReviewedProduct AS reviews, Products AS descriptions
                            WHERE reviews.user_id = :user_id
                            AND reviews.product_id = descriptions.id)
                            ORDER BY time_reviewed DESC LIMIT 5''', user_id = user_id)
        
        return [FeedbackItem(*row) for row in rows] if rows else None