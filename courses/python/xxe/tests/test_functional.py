import pytest
import uuid
import io
from random import randint


class TestXmlFunctional:

    def _process_xml_body(self, client):
        xml_body = ""
        products = list()
        total_sum = 0.0
        for i in range(randint(1, 10)):
            product = {'name': str(uuid.uuid4()), 'quantity': randint(1, 999), 'price': float(randint(1, 10000)) / 100}
            products.append(product)
            total_sum += product.get('quantity') * product.get('price')
            xml_body += '''<product id="%d">
                    <name>%s</name>
                    <quantity>%d</quantity>
                    <price>%0.2f</price>
                </product>''' % (i, product.get('name'), product.get('quantity'), product.get('price'))
        xml_body = '<bill>' + xml_body + '</bill>'
        response = client.post("/",
                               data={'bill': (io.BytesIO(xml_body.encode('utf-8')), 'bill.xml')},
                               content_type='multipart/form-data')
        return products, total_sum, response.data.decode('utf-8')

    def xml_processing(self, client):
        products, _, response = self._process_xml_body(client)
        for product in products:
            if product.get('name') not in response:
                return False, "XML processing is broken."
        return True, "XML processing - OK"

    def cost_calculation(self, client):
        _, total_sum, response = self._process_xml_body(client)
        if str(total_sum) not in response:
            return False, "Total cost calculation is broken."
        return True, "Total cost calculation - OK"

    def test_vulnerable_xml_processing(self, vulnerable_client):
        (success,_) = self.xml_processing(vulnerable_client)
        assert success, 'XML processing is broken in vulnerable app.'

    def test_patched_xml_processing(self, patched_client):
        (success, _) = self.xml_processing(patched_client)
        assert success, 'XML processing is broken in patched app.'

    def test_vulnerable_cost_calculation(self, vulnerable_client):
        (success,_) = self.cost_calculation(vulnerable_client)
        assert success, 'Cost calculation is broken in vulnerable app.'

    def test_patched_cost_calculation(self, patched_client):
        (success, _) = self.cost_calculation(patched_client)
        assert success, 'Cost calculation is broken in patched app.'
