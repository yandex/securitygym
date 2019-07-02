import pytest
import uuid
import io
import tempfile
import os


class TestXmlSecurity:

    def xxe_protection(self, client):
        random_string = str(uuid.uuid4())
        tmp_fd, tmp_path = tempfile.mkstemp()
        with open(tmp_path, 'w') as f:
            f.write(random_string)
        os.close(tmp_fd)
        xml_body = '''<!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file://%s">]>
            <bill>
                <product id="28">
                    <name>&xxe;</name>
                    <quantity>1</quantity>
                    <price>1337</price>
                </product>
            </bill>
            ''' % tmp_path
        response = client.post("/",
                               data={'bill': (io.BytesIO(xml_body.encode('utf-8')), 'bill.xml')},
                               content_type='multipart/form-data')
        os.unlink(tmp_path)
        if random_string in response.data.decode('utf-8'):
            return False, "Bill processing is vulnerable to XXE"
        return True, "Bill processing is not vulnerable to XXE"

    def test_vulnerable_xxe_protection(self, vulnerable_client):
        (patched, _) = self.xxe_protection(vulnerable_client)
        assert not patched, 'XML processing is not vulnerable to XXE in vulnerable app.'

    def test_patched_xxe_protection(self, patched_client):
        (patched, _) = self.xxe_protection(patched_client)
        assert patched, 'XML processing is vulnerable to XXE in patched app.'
