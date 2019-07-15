import os
import tempfile
import re

import pytest

from csrf.vuln_app import create_app


@pytest.fixture
def vulnerable_app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"VULNERABLE": True, "DATABASE": db_path})
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def patched_app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"VULNERABLE": False, "DATABASE": db_path})
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def vulnerable_client(vulnerable_app):
    return vulnerable_app.test_client()


@pytest.fixture
def patched_client(patched_app):
    return patched_app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, username="test", password="test"):
        return self._client.post(
            "/auth/register", data={"username": username, "password": password}
        )

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")

    def csrf_token(self, path):
        rv = self._client.get(path)
        m = re.search(r"(<input[^>]+name=\"csrf_token\"[^>]+value=\")([-A-Za-z.0-9_]+)",
                      rv.data.decode("utf-8"))
        if m:
            return m.group(2)
        else:
            m = re.search(r"(<input[^>]+value=\")([-A-Za-z.0-9_]+)([^>]+name=\"csrf_token\"[^>])",
                          rv.data.decode("utf-8"))
            if m:
                return m.group(2)
            return ''


@pytest.fixture
def vulnerable_auth(vulnerable_client):
    return AuthActions(vulnerable_client)


@pytest.fixture
def patched_auth(patched_client):
    return AuthActions(patched_client)