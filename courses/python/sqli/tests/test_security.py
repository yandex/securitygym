import pytest
import uuid
from random import randint
from sqli.vuln_app.db import get_db


class TestSQLSecurity():

    def sqli_in_title_protection(self, app, client):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            random_title = str(uuid.uuid4())
            random_content = str(uuid.uuid4())
            cursor.execute("INSERT INTO article (title, content, created_at) VALUES (?, ?, date('now'))",
                           (random_title, random_content)
                           )
            db.commit()
            payloads = ['\' or 1=1 --', '\' and 1=1 --', '" or 1=1 --', '" and 1=1 --',
                        '` or 1=1 --', '` and 1=1 --', '\') or 1=1 --', '") or 1=1 --', '`) or 1=1 --',
                        '\')) or 1=1 --', '")) or 1=1 --', '`)) or 1=1 --',
                        '\'))) or 1=1 --', '"))) or 1=1 --', '`))) or 1=1 --']
            for payload in payloads:
                resp = client.post("/", data={'title': random_title + payload, 'order': 'ASC'}).data.decode('utf-8')
                if random_content in resp:
                    return False, 'Article search is vulnerable to SQL injection in TITLE parameter'
        return True, 'Article search is not vulnerable to SQL injection in TITLE parameter'

    def sqli_in_order_protection(self, app, client):
        articles = []
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            random_prefix = str(uuid.uuid4())
            for _ in range(randint(10,20)):
                random_title = str(uuid.uuid4()) + random_prefix + str(uuid.uuid4())
                random_content = str(uuid.uuid4())
                random_datetime = randint(1546300800, 1551398400)
                articles.append((random_title, random_content, random_datetime))
                cursor.execute("INSERT INTO article (title, content, created_at) VALUES (?, ?, datetime(?, 'unixepoch'))",
                               (random_title, random_content, random_datetime)
                               )
            db.commit()
            for order_by in ["DESC LIMIT " + str (len(articles) - randint(3,7)),
                             "ASC LIMIT " + str (len(articles) - randint(3,7))]:
                resp = client.post("/", data={'title': random_prefix, 'order': order_by}).data.decode('utf-8')
                for (_, content, _) in articles:
                    if content not in resp:
                        return False, 'Article search is vulnerable to SQL injection in ORDER parameter'
        return True, 'Article search is not vulnerable to SQL injection in ORDER parameter'

    def test_vulnerable_sqli_in_title_protection(self, vulnerable_app, vulnerable_client):
        (patched,_) = self.sqli_in_title_protection(vulnerable_app, vulnerable_client)
        assert not patched, 'Articles search is not vulnerable to SQL injection in TITLE parameter in vulnerable app.'

    def test_patched_sqli_in_title_protection(self, patched_app, patched_client):
        (patched, _) = self.sqli_in_title_protection(patched_app, patched_client)
        assert patched, 'Articles search is vulnerable to SQL injection in TITLE parameter in patched app.'

    def test_vulnerable_sqli_in_order_protection(self, vulnerable_app, vulnerable_client):
        (patched,_) = self.sqli_in_order_protection(vulnerable_app, vulnerable_client)
        assert not patched, 'Articles search is not vulnerable to SQL injection in ORDER parameter in vulnerable app.'

    def test_patched_sqli_in_order_protection(self, patched_app, patched_client):
        (patched, _) = self.sqli_in_order_protection(patched_app, patched_client)
        assert patched, 'Articles search is vulnerable to SQL injection in ORDER parameter in patched app.'
