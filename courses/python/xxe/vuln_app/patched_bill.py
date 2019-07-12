from flask import Blueprint
from flask import render_template
from flask import request

from lxml import etree

bp = Blueprint("bill", __name__)


class Product:
    def __init__(self, name = "", quantity = 0, price = 0.0):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return "\"Name:%s, Price:%0.2f, Quantity:%d\"" % (self.name, self.price, self.quantity)

    def __eq__(self, other):
        return self.name == other.name and self.quantity == other.quantity and abs(self.price - other.price) < 0.01


def bill_process(xml_data):
    parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False, no_network=True)
    bill = etree.fromstring(xml_data, parser)
    products = list()
    for product in bill.getchildren():
        product_dict = {}
        for prop in product.getchildren():
            text = prop.text if prop.text else ""
            product_dict[prop.tag] = text
        if product.tag == "product":
            products.append(Product(name=product_dict.get("name"),
                                    quantity=int(product_dict.get("quantity")),
                                    price=float(product_dict.get("price"))))

    return products


def calculate_total_cost(products):
    total_cost = 0.0
    for product in products:
        total_cost += product.quantity * product.price
    return total_cost


@bp.route("/", methods=("GET", "POST"))
def process():
    if request.method == "POST":
        file = request.files['bill']
        if file:
            xml_content = file.read().decode('utf-8')
            products = bill_process(xml_content)
            return render_template("bill/report.html", products=products, total_cost=calculate_total_cost(products))
    return render_template("bill/form.html")
