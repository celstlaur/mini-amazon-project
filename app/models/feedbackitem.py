from flask import current_app as app
import datetime

class FeedbackItem:
    def __init__(self, reviewed, reviewed_id, reviewed_type, review, timestamp):
        self.reviewed = reviewed
        self.reviewed_id = reviewed_id
        self.reviewed_type = reviewed_type
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
                            (SELECT names.firstname AS reviewed, reviews.seller_id AS reviewed_id, 'Seller' AS reviewed_type, reviews.review, time_reviewed_seller AS time_reviewed
                            FROM ReviewedSeller AS reviews, Users AS names
                            WHERE reviews.user_id = :user_id
                            AND reviews.seller_id = names.id)
                            UNION
                            (SELECT descriptions.name AS reviewed, reviews.product_id AS reviewed_id, 'Product' AS reviewed_type, reviews.review, time_reviewed_product AS time_reviewed
                            FROM ReviewedProduct AS reviews, Products AS descriptions
                            WHERE reviews.user_id = :user_id
                            AND reviews.product_id = descriptions.id)
                            ORDER BY time_reviewed DESC''', user_id = user_id)
        
        return [FeedbackItem(*row) for row in rows] if rows else None
    
    @staticmethod
    def get_product_reviews(user_id):
        rows = app.db.execute('''
                            SELECT *
                            FROM ReviewedProduct
                            WHERE user_id = :user_id''', user_id = user_id)
        
        return [FeedbackItem(*row) for row in rows] if rows else None
    
    @staticmethod
    def get_seller_reviews(user_id):
        rows = app.db.execute('''
                            SELECT *
                            FROM ReviewedSeller
                            WHERE user_id = :user_id''', user_id = user_id)
        
        return [FeedbackItem(*row) for row in rows] if rows else None
    
    @staticmethod
    def add_product_feedback(uid, pid, review):
        try:
            current_time = datetime.datetime.now()
            rows = app.db.execute("""INSERT INTO ReviewedProduct(user_id, product_id, review, time_reviewed_product)
                                VALUES(:user_id, :product_id, :review, :time_reviewed_product)""",
                                  user_id=uid,
                                  product_id=pid,
                                  review=review,
                                  time_reviewed_product=current_time)
            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def delete_product_feedback(uid, pid, review):
        try:
            rows = app.db.execute("""DELETE FROM ReviewedProduct
                                WHERE user_id = :uid AND product_id = :pid AND review = :review""",
                                  uid=uid,
                                  pid=pid,
                                  review=review)
            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return e
    
    @staticmethod
    def delete_seller_feedback(uid, sid, review):
        try:
            rows = app.db.execute("""DELETE FROM ReviewedSeller
                                WHERE user_id = :uid AND seller_id = :sid AND review = :review""",
                                  uid=uid,
                                  sid=sid,
                                  review=review)
            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return e
        
    @staticmethod
    def edit_product_feedback(uid, pid, newReview):
        try:
            rows = app.db.execute("""UPDATE ReviewedProduct
                                SET review = :newReview
                                WHERE user_id = :uid AND product_id = :pid""",
                                  uid=uid,
                                  pid=pid,
                                  newReview=newReview)
            #id = rows[0][0]
            #return FeedbackItem.get_all(id)
            return True
        except Exception as e:
            print(str(e))
            return e