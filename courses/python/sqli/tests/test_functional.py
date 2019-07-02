import pytest
import uuid
from random import randint
from sqli.vuln_app.db import get_db


class TestArticlesSearchFunctional():

    def articles_search_one(self, app, client):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            random_title = str(uuid.uuid4())
            random_content = str(uuid.uuid4())
            cursor.execute("INSERT INTO article (title, content, created_at) VALUES (?, ?, date('now'))",
                           (random_title, random_content)
                           )
            db.commit()
        for order_by in ['DESC', 'ASC']:
            resp = client.post("/", data={'title': random_title, 'order': order_by})
            if random_content not in resp.data.decode('utf-8'):
                return False, "Articles search is broken. Article not found"
        return True, "Articles search - OK"

    def articles_order(self, app, client):
        search_articles = []
        not_search_articles = []
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            random_prefix = str(uuid.uuid4())
            for _ in range(randint(3, 10)):
                random_title = str(uuid.uuid4()) + random_prefix + str(uuid.uuid4())
                random_content = str(uuid.uuid4())
                random_datetime = randint(1546300800, 1551398400)
                search_articles.append((random_title, random_content, random_datetime))
                cursor.execute("INSERT INTO article (title, content, created_at) VALUES (?, ?, datetime(?, 'unixepoch'))",
                               (random_title, random_content, random_datetime)
                               )
            for _ in range(randint(3, 10)):
                random_title = str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4())
                random_content = str(uuid.uuid4())
                random_datetime = randint(1546300800, 1551398400)
                not_search_articles.append((random_title, random_content, random_datetime))
                cursor.execute("INSERT INTO article (title, content, created_at) VALUES (?, ?, datetime(?, 'unixepoch'))",
                               (random_title, random_content, random_datetime)
                               )
            db.commit()
            # search ASC order
            search_articles.sort(key=lambda article: article[2])
            resp_content = client.post("/", data={'title': random_prefix, 'order': 'ASC'}).data.decode('utf-8')
            for (_, content, _) in search_articles:
                if content not in resp_content:
                    return False, "Articles search is broken. Articles in wrong order"
                resp_content = resp_content[resp_content.find(content):]
            search_articles.reverse()
            # search DESC order
            resp_content = client.post("/", data={'title': random_prefix, 'order': 'DESC'}).data.decode('utf-8')
            for (_, content, _) in search_articles:
                if content not in resp_content:
                    return False, "Articles search is broken. Articles in wrong order"
                resp_content = resp_content[resp_content.find(content):]
            # not_search_articles not in list
            resp_content = client.post("/", data={'title': random_prefix, 'order': 'DESC'}).data.decode('utf-8')
            for (_, content, _) in not_search_articles:
                if content in resp_content:
                    return False, "Articles search is broken. Additional articles found"
                resp_content = resp_content[resp_content.find(content):]
            return True, "Articles search order - OK"

    def test_vulnerable_articles_search_one(self, vulnerable_app, vulnerable_client):
        (success,_) = self.articles_search_one(vulnerable_app, vulnerable_client)
        assert success, 'Articles search is broken in vulnerable app.'

    def test_patched_articles_search_one(self, patched_app, patched_client):
        (success, _) = self.articles_search_one(patched_app, patched_client)
        assert success, 'Articles search is broken in patched app.'

    def test_vulnerable_articles_order(self, vulnerable_app, vulnerable_client):
        (success,_) = self.articles_order(vulnerable_app, vulnerable_client)
        assert success, 'Articles search order is broken in vulnerable app.'

    def test_patched_articles_order(self, patched_app, patched_client):
        (success, _) = self.articles_order(patched_app, patched_client)
        assert success, 'Articles search order is broken in patched app.'
