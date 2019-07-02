import pytest
from mflac.tests.base_mflac import BaseMFLACTest
import uuid
from random import randint


class TestAdminPanelFunctional(BaseMFLACTest):

    def admin_users_list(self, app, client, auth):
        for _ in range(randint(1, 3)):
            admin_username = str(uuid.uuid4())
            admin_password = str(uuid.uuid4())
            self._add_user(app, admin_username, admin_password, True)
            auth.login(admin_username, admin_password)
            for _ in range(randint(1, 3)):
                user_username = str(uuid.uuid4())
                user_password = str(uuid.uuid4())
                self._add_user(app, user_username, user_password, False)
                resp = client.get("/admin/users_list")
                if user_username not in resp.data.decode('utf-8'):
                    return False, "Admin panel is broken. Registered user is not found in list."
        return True, "Admin panel - OK"

    def test_vulnerable_admin_users_list(self, vulnerable_app, vulnerable_client, vulnerable_auth):
        (success,_) = self.admin_users_list(vulnerable_app, vulnerable_client, vulnerable_auth)
        assert success, 'Admin panel is broken in vulnerable app.'

    def test_patched_admin_users_list(self, patched_app, patched_client, patched_auth):
        (success, _) = self.admin_users_list(patched_app, patched_client, patched_auth)
        assert success, 'Admin panel is broken in patched app.'
