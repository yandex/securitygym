from csrf.vuln_app.db import get_db
from werkzeug.security import generate_password_hash
import re


class BaseCSRFTest:
    @staticmethod
    def _add_user(app, username, password, balance):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO user (username, password, balance) VALUES (?, ?, ?)",
                           (username, generate_password_hash(password), balance)
                           )
            db.commit()
            return cursor.lastrowid

    @staticmethod
    def _add_payment(app, from_user_id, to_user_id, amount):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO payment (from_user_id, to_user_id, amount, created_at) "
                           "VALUES (?, ?, ?, date('now'))",
                           (from_user_id, to_user_id, amount)
                           )
            db.commit()
            return cursor.lastrowid
