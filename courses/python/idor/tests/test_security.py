import pytest
from idor.tests.base_idor import BaseIDORTest
import uuid
from random import randint


class TestPaymentSecurity(BaseIDORTest):

    def payment_details_idor(self, app, client, auth):
        for _ in range(randint(1, 3)):
            first_username = str(uuid.uuid4())
            first_password = str(uuid.uuid4())
            first_user_id = self._add_user(app, first_username, first_password)
            for _ in range(randint(1, 3)):
                payment_description = str(uuid.uuid4())
                payment_id = self._add_payment(app, first_user_id, randint(1, 999), payment_description)
                second_username = str(uuid.uuid4())
                second_password = str(uuid.uuid4())
                self._add_user(app, second_username, second_password)
                auth.login(second_username, second_password)
                resp = client.get("/payment/"+str(payment_id))
                if payment_description in resp.data.decode('utf-8'):
                    return False, "Payment Details is vulnerable to IDOR."
        return True, "Payment Details is not vulnerable"

    def test_vulnerable_payment_details_idor(self, vulnerable_app, vulnerable_client, vulnerable_auth):
        (patched_from_IDOR,_) = self.payment_details_idor(vulnerable_app, vulnerable_client, vulnerable_auth)
        assert patched_from_IDOR == False, 'Payment Details is not vulnerable to IDOR in vulnerable app.'

    def test_patched_payment_details_idor(self, patched_app, patched_client, patched_auth):
        (patched_from_IDOR, _) = self.payment_details_idor(patched_app, patched_client, patched_auth)
        assert patched_from_IDOR, 'Payment Details is vulnerable to IDOR in patched app.'
