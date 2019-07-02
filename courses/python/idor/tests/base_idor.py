from idor.vuln_app.db import get_db
from werkzeug.security import generate_password_hash


class BaseIDORTest:
    @staticmethod
    def _add_user(app, username, password):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                           (username, generate_password_hash(password))
                           )
            db.commit()
            return cursor.lastrowid

    @staticmethod
    def _add_payment(app, user_id, amount, description):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO payment (user_id, amount, description) VALUES (?, ?, ?)",
                           (user_id, amount, description)
                           )
            db.commit()
            return cursor.lastrowid