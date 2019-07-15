import uuid
from random import randint


class TestBadgeGeneratorSecurity:

    def ssti_protection(self, client):
        begin = str(uuid.uuid4())
        first_num = randint(1, 1000)
        second_num = randint(1, 1000)
        end = str(uuid.uuid4())
        payload = begin + '{{ ' + str(first_num) + '*' + str(second_num) + ' }}' + end
        response = client.post("/",
                               data={'username': payload})

        if str(first_num * second_num) in response.data.decode('utf-8'):
            return False, "Badge generation is vulnerable to SSTI"
        if payload not in response.data.decode('utf-8'):
            return False, "Badge generation is vulnerable to SSTI"
        return True, "Badge generation SSTI protection - OK"

    def xss_protection(self, client):
        payload = "<" + str(uuid.uuid4()) + ">"
        response = client.post("/",
                               data={'username': payload})

        if payload in response.data.decode('utf-8'):
            return False, "Badge generation is vulnerable to XSS"
        return True, "Badge generation XSS protection - OK"

    def test_vulnerable_ssti_protection(self, vulnerable_client):
        (success,_) = self.ssti_protection(vulnerable_client)
        assert not success, 'Badge generation is not vulnerable to SSTI in vulnerable app.'

    def test_patched_ssti_protection(self, patched_client):
        (success, _) = self.ssti_protection(patched_client)
        assert success, 'Badge generation is vulnerable to SSTI in patched app.'

    def test_vulnerable_xss_protection(self, vulnerable_client):
        (success,_) = self.xss_protection(vulnerable_client)
        assert not success, 'Badge generation is not vulnerable to XSS in vulnerable app.'

    def test_patched_xss_protection(self, patched_client):
        (success, _) = self.xss_protection(patched_client)
        assert success, 'Badge generation is vulnerable to XSS in patched app.'
