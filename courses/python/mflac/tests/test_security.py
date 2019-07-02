import pytest
from mflac.tests.base_mflac import BaseMFLACTest
import uuid
from random import randint


class TestAdminPanelSecurity(BaseMFLACTest):

    def admin_users_list(self, app, client, auth):
        for _ in range(randint(1, 3)):
            first_username = str(uuid.uuid4())
            second_password = str(uuid.uuid4())
            self._add_user(app, first_username, second_password, randint(0,1) == 1)
            for _ in range(randint(1, 3)):
                user_username = str(uuid.uuid4())
                user_password = str(uuid.uuid4())
                self._add_user(app, user_username, user_password, False)
                auth.login(user_username, user_password)
                resp = client.get("/admin/users_list")
                if first_username in resp.data.decode('utf-8'):
                    return False, "Admin panel is vulnerable. Access control is broken"
        return True, "Admin panel is not vulnerable"

    def test_vulnerable_admin_users_list(self, vulnerable_app, vulnerable_client, vulnerable_auth):
        (patched_from_MFLAC, _) = self.admin_users_list(vulnerable_app, vulnerable_client, vulnerable_auth)
        assert patched_from_MFLAC == False, 'Admin panel is not vulnerable to MFLAC in vulnerable app.'

    def test_patched_admin_users_list(self, patched_app, patched_client, patched_auth):
        (patched_from_MFLAC, _) = self.admin_users_list(patched_app, patched_client, patched_auth)
        assert patched_from_MFLAC, 'Admin panel is vulnerable to MFLAC in patched app.'
