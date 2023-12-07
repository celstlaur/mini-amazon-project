from flask_login import UserMixin
from flask import current_app as app

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname)
VALUES(:email, :password, :firstname, :lastname)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]

            current_time = datetime.utcnow()
            app.db.execute('''
                INSERT INTO Balance (user_id, balance_timestamp, balance)
                VALUES (:user_id, :balance_timestamp, :balance)
            ''',
            user_id=id,
            balance_timestamp=current_time,
            balance=0)

            
            
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
               
    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
    

    @staticmethod
    def is_seller(id):
        rows = app.db.execute("""
    SELECT id
    FROM Sellers
    WHERE id = :id
    """,
                                id=id)
        if len(rows) != 1:
            return False
        return True
    
    
    @staticmethod
    def has_cart(id):
        rows = app.db.execute("""
    SELECT user_id
    FROM CartContents
    WHERE user_id = :id
    """,
                                id=id)
        return len(rows) > 0
    
    @staticmethod
    def get_address(id):
        rows = app.db.execute("""
    SELECT address
    FROM UserAddress
    WHERE id = :id
    """,
                                id=id)
        return rows
    
    @staticmethod
    def num_sales(id):
        rows = app.db.execute("""
    SELECT order_id
    FROM Fulfills
    WHERE seller_id = :id
    """,
                                id=id)
        return len(rows)

    @staticmethod
    def num_purchases(id):
        rows = app.db.execute("""
    SELECT id
    FROM OrderFact
    WHERE buyer_id = :id
    """,
                                id=id)
        return len(rows)


