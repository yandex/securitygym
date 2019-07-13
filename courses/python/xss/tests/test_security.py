import uuid
from xss.vuln_app.db import get_db


class TestGuestbookSecurity():

    def xss_protection(self, app, client):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            random_beginning = str(uuid.uuid4())
            random_payload = '<'+str(uuid.uuid4())[0]+'>'
            random_ending = str(uuid.uuid4())
            cursor.execute("INSERT INTO messages (message, created_at) VALUES (?, date('now'))",
                           (random_beginning + random_payload + random_ending,))
            db.commit()
        resp = client.get("/")
        if random_payload in resp.data.decode('utf-8'):
            return False, "Guestbook is vulnerable to XSS"
        return True, "Guestbook is not vulnerable to XSS"

    def test_vulnerable_xss_protection(self, vulnerable_app, vulnerable_client):
        (success, _) = self.xss_protection(vulnerable_app, vulnerable_client)
        assert not success, 'Guestbook is not vulnerable to xss in vulnerable app'

    def test_patched_xss_protection(self, patched_app, patched_client):
        (success, _) = self.xss_protection(patched_app, patched_client)
        assert success, 'Guestbook is vulnerable to xss in patched app'
