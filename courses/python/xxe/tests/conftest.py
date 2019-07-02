import os
import tempfile

import pytest

from xxe.vuln_app import create_app


@pytest.fixture
def vulnerable_app():
    app = create_app({"VULNERABLE": True})
    yield app


@pytest.fixture()
def patched_app():
    app = create_app({"VULNERABLE": False})
    yield app


@pytest.fixture
def vulnerable_client(vulnerable_app):
    return vulnerable_app.test_client()


@pytest.fixture
def patched_client(patched_app):
    return patched_app.test_client()
