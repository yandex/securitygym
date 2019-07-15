from csrf.tests.base_csrf import BaseCSRFTest
from csrf.vuln_app.db import get_db

import uuid
from random import randint


class TestCSRFProtection(BaseCSRFTest):

    def send_csrf_protection(self, app, client, auth):
        from_username = str(uuid.uuid4())
        from_passwd = str(uuid.uuid4())
        from_balance = randint(100, 10000)
        from_uid = BaseCSRFTest._add_user(app, from_username, from_passwd, from_balance)
        to_username = str(uuid.uuid4())
        to_passwd = str(uuid.uuid4())
        to_balance = randint(100, 10000)
        to_uid = BaseCSRFTest._add_user(app, to_username, to_passwd, to_balance)
        auth.login(to_username, to_passwd)
        incorrect_csrf_token = auth.csrf_token("/send")
        auth.logout()
        auth.login(from_username, from_passwd)
        amount = randint(1, from_balance)
        client.post("/send", data={'to_user_id': to_uid, 'amount': amount, 'csrf_token': incorrect_csrf_token})
        with app.app_context():
            db = get_db()
            # check balances
            new_from_balance = db.execute("SELECT balance FROM user WHERE id = ?", (from_uid,)).fetchone()["balance"]
            new_to_balance = db.execute("SELECT balance FROM user WHERE id = ?", (to_uid,)).fetchone()["balance"]
            if new_from_balance == from_balance - amount or new_to_balance == to_balance + amount:
                return False, "Send payment is vulnerable to CSRF attack"
        return True, "CSRF protection is OK"
        csrf_token = self._get_csrf_token(app, client, auth, "/send")
        return self._send_payment(app, client, auth, csrf_token)

    def test_vulnerable_payment_details(self, vulnerable_app, vulnerable_client, vulnerable_auth):
        (success,_) = self.send_csrf_protection(vulnerable_app, vulnerable_client, vulnerable_auth)
        assert not success, 'Application is not vulnerable to CSRF in vulnerable app'

    def test_patched_payment_details(self, patched_app, patched_client, patched_auth):
        (success, _) = self.send_csrf_protection(patched_app, patched_client, patched_auth)
        assert success, 'Application is vulnerable to CSRF in patched app'
