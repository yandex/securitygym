import pytest
from idor.tests.base_idor import BaseIDORTest
import uuid
from random import randint


class TestPaymentFunctional(BaseIDORTest):

    def payment_details(self, app, client, auth):
        for _ in range(randint(1, 3)):
            username = str(uuid.uuid4())
            password = str(uuid.uuid4())
            user_id = self._add_user(app, username, password)
            for _ in range(randint(1, 3)):
                payment_description = str(uuid.uuid4())
                payment_id = self._add_payment(app, user_id, randint(1, 999), payment_description)
                auth.login(username, password)
                resp = client.get("/payment/"+str(payment_id))
                if payment_description not in resp.data.decode('utf-8'):
                    return False, "Payment Details is broken. Description not found"
        return True, "Payment Details - OK"

    def test_vulnerable_payment_details(self, vulnerable_app, vulnerable_client, vulnerable_auth):
        (success,_) = self.payment_details(vulnerable_app, vulnerable_client, vulnerable_auth)
        assert success, 'Payment Details is broken in vulnerable app.'

    def test_patched_payment_details(self, patched_app, patched_client, patched_auth):
        (success, _) = self.payment_details(patched_app, patched_client, patched_auth)
        assert success, 'Payment Details is broken in patched app.'
