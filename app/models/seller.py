from flask import current_app as app

class Seller:
    def __init__(self, user_id, business_email, business_address):
        self.user_id = user_id
        self.business_email = business_email
        self.business_address = business_address
        
    @staticmethod
    def seller_details(user_id):
       
        rows = app.db.execute('''
    SELECT *
    FROM Sellers
    WHERE id = :user_id
    ''',
                              user_id=user_id)
        return [Seller(*row) for row in rows] if rows else None
    
    
    @staticmethod
    def become_seller(id, email_address, business_address):
        try:
            app.db.execute('''
                INSERT INTO Sellers (id, email_address, business_address)
                VALUES (:id, :email_address, :business_address)
            ''',
            id=id,
            email_address=email_address,
            business_address=business_address)

            return Seller.seller_details(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
            