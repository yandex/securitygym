from mflac.vuln_app.db import get_db
from werkzeug.security import generate_password_hash


class BaseMFLACTest:
    @staticmethod
    def _add_user(app, username, password, is_admin):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?)",
                           (username, generate_password_hash(password), is_admin)
                           )
            db.commit()
            return cursor.lastrowid
