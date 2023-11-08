from flask import current_app as app


class Balance:
    def __init__(self, user_id, balance_timestamp, balance):
        self.user_id = user_id
        self.balance_timestamp = balance_timestamp
        self.balance = balance

    @staticmethod
    def current_balance(user_id):
        rows = app.db.execute('''
SELECT balance 
FROM Balance 
WHERE user_id = :user_id 
ORDER BY balance_timestamp DESC 
LIMIT 1
''',
                              user_id=user_id)
        return Balance(*(rows[0]))
    
    @staticmethod
    def get_all_balance_by_uid(user_id):
        rows = app.db.execute('''
SELECT user_id, balance_timestamp, balance
FROM Balance
WHERE user_id = :user_id
ORDER BY balance_timestamp DESC
''',
                              user_id=user_id)
        return [Balance(*row) for row in rows]