import pytest
import uuid
import io
import tempfile
import os


class TestYAMLSecurity:

    def yaml_protection(self, client):
        random_string = str(uuid.uuid4())
        tmp_fd, tmp_path = tempfile.mkstemp()
        yaml_file = "test: !!python/object/apply:os.system ['echo "+random_string+" > "+tmp_path+"']"
        client.post("/", data={'file': (io.BytesIO(yaml_file.encode('utf-8')), str(uuid.uuid4()) + '.yaml')},
                    content_type='multipart/form-data')
        tmp_content = open(tmp_path).read()
        os.close(tmp_fd)
        os.unlink(tmp_path)
        if random_string in tmp_content:
            return False, "YAML processing is vulnerable to insecure deserialization"
        return True, "YAML processing is not vulnerable to insecure deserialization"

    def test_vulnerable_yaml_protection(self, vulnerable_client):
        (patched, _) = self.yaml_protection(vulnerable_client)
        assert not patched, 'YAML processing is not vulnerable to insecure deserialization in vulnerable app.'

    def test_patched_yaml_protection(self, patched_client):
        (patched, _) = self.yaml_protection(patched_client)
        assert patched, 'XML processing is vulnerable to insecure deserialization in patched app.'
