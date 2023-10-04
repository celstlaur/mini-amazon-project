from flask import current_app as app
import datetime


class Wish:
    def __init__(self, id, uid, pid, time_added):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_added = time_added

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE id = :id
''',
                              id=id)
        return Wish(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE uid = :uid
ORDER BY time_added DESC
''',
                              uid=uid)
        return [Wish(*row) for row in rows]


    @staticmethod
    def add_to_wishlist(uid, pid):
        try:
            current_time = datetime.datetime.now()
            rows = app.db.execute("""
INSERT INTO Wishes(uid, pid, time_added)
VALUES(:uid, :pid, :time_added)
RETURNING id
""",
                                  uid=uid,
                                  pid=pid,
                                  time_added=current_time)
            id = rows[0][0]
            return Wish.get(id)
        except Exception as e:
            print(str(e))
            return None
