import os
import tempfile

import pytest

from xss.vuln_app import create_app


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
