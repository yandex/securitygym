import pytest
import uuid
import io
from random import randint
import yaml


class TestYAMLFunctional:

    def yaml_processing(self, client):
        yaml_dict = dict()
        for _ in range(randint(5,10)):
            yaml_dict[str(uuid.uuid4())] = str(uuid.uuid4())
        yaml_file = yaml.dump(yaml_dict)
        response = client.post("/",
                               data={'file': (io.BytesIO(yaml_file.encode('utf-8')), str(uuid.uuid4()) + '.yaml')},
                               content_type='multipart/form-data').data.decode('utf-8')
        for key, value in yaml_dict.items():
            if '<b>'+key+'</b>' not in response:
                return False, "YAML processing is broken."
            if value not in response:
                return False, "YAML processing is broken."
        return True, "YAML processing - OK"

    def test_vulnerable_yaml_processing(self, vulnerable_client):
        (success,_) = self.yaml_processing(vulnerable_client)
        assert success, 'YAML processing is broken in vulnerable app.'

    def test_patched_yaml_processing(self, patched_client):
        (success, _) = self.yaml_processing(patched_client)
        assert success, 'YAML processing is broken in patched app.'
