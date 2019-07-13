import uuid
from xss.vuln_app.db import get_db


class TestGuestbookFunctional():

    def show_formatted_message(self, app, client):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            random_beginning = str(uuid.uuid4())
            random_ending = str(uuid.uuid4())
            cursor.execute("INSERT INTO messages (message, created_at) VALUES (?, date('now'))",
                           (random_beginning + 'guestbook' + random_ending,))
            db.commit()
        random_message = random_beginning + '<b>guestbook</b>' + random_ending
        resp = client.get("/")
        if random_message not in resp.data.decode('utf-8'):
            return False, "Guestbook formating is broken"
        return True, "Guestbook formating - OK"

    def test_vulnerable_show_formatted_message(self, vulnerable_app, vulnerable_client):
        (success, _) = self.show_formatted_message(vulnerable_app, vulnerable_client)
        assert success, 'Guestbook formating is broken in vulnerable app.'

    def test_patched_show_formatted_message(self, patched_app, patched_client):
        (success, _) = self.show_formatted_message(patched_app, patched_client)
        assert success, 'Guestbook formating is broken in patched app.'
