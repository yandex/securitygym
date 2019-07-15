import uuid


class TestBadgeGeneratorFunctional:

    def badge_generation(self, client):
        username = str(uuid.uuid4())
        response = client.post("/",
                               data={'username': username})
        if ('<p><h3>%s</h3>' % username) not in response.data.decode('utf-8'):
            return False, "Badge generation is broken."
        return True, "Badge generation - OK"

    def badge_generation_with_brace(self, client):
        username = str(uuid.uuid4())
        payload = str(uuid.uuid4())+"{{ '"+username+"' }}"+str(uuid.uuid4())
        response = client.post("/",
                               data={'username': payload})
        if username not in response.data.decode('utf-8'):
            return False, "Badge generation with brace is broken."
        return True, "Badge generation with brace - OK"

    def badge_generation_with_bracket(self, client):
        username = str(uuid.uuid4())
        payload = "<" + str(uuid.uuid4()) + "/>" + username
        response = client.post("/",
                               data={'username': payload})
        if username not in response.data.decode('utf-8'):
            return False, "Badge generation with bracket is broken."
        return True, "Badge generation with bracket - OK"

    def test_vulnerable_badge_generation(self, vulnerable_client):
        (success,_) = self.badge_generation(vulnerable_client)
        assert success, 'Badge generation is broken in vulnerable app.'

    def test_patched_badge_generation(self, patched_client):
        (success, _) = self.badge_generation(patched_client)
        assert success, 'Badge generation is broken in patched app.'

    def test_vulnerable_badge_generation_with_brace(self, vulnerable_client):
        (success,_) = self.badge_generation_with_brace(vulnerable_client)
        assert success, 'Badge generation with brace is broken in vulnerable app.'

    def test_patched_badge_generation_with_brace(self, patched_client):
        (success, _) = self.badge_generation_with_brace(patched_client)
        assert success, 'Badge generation with brace is broken in patched app.'

    def test_vulnerable_badge_generation_with_bracket(self, vulnerable_client):
        (success,_) = self.badge_generation_with_bracket(vulnerable_client)
        assert success, 'Badge generation with bracket is broken in vulnerable app.'

    def test_patched_badge_generation_with_bracket(self, patched_client):
        (success, _) = self.badge_generation_with_bracket(patched_client)
        assert success, 'Badge generation with bracket is broken in patched app.'
