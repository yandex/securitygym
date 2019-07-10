const lesson = {
    "python_xxe": {
"code": `from lxml import etree


class Product:
    def __init__(self, name = "", quantity = 0, price = 0.0):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return "\\"Name:%s, Price:%0.2f, Quantity:%d\\"" % (self.name, self.price, self.quantity)

    def __eq__(self, other):
        return self.name == other.name and self.quantity == other.quantity and abs(self.price - other.price) < 0.01


def bill_process(xml_data):
    bill = etree.fromstring(xml_data)
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


def calculate_total_sum(products):
    total_sum = 0.0
    for product in products:
        total_sum += product.quantity * product.price
    return total_sum


def process_request(xml_data):
    products = bill_process(xml_data)
    total_sum = calculate_total_sum(products)
    return {"total_sum": total_sum, "products": products}
`,
"md":`## Атака «XML External Entity (XXE)»

XML External Entity (XXE) — это тип атаки на приложение, которое производит обработку XML. 
Данная атака возможна, когда XML-парсер поддерживает возможность обрабатывать внешние сущности. 
Это может привести к раскрытию конфиденциальной информации, чтению файлов, SSRF и другим серьёзным проблемам безопасности.

**Если вы используете XML парсер для недоверенных данных:**
* Проверьте возможность подключения  \`\`\`DTD схем\`\`\` или  \`\`\`External Entities\`\`\`;
* Если данная возможность включена, **явно выключите её**;
* Обратите внимание на аналогичные риски при [работе с документами в rich-форматах](https://wiki.yandex-team.ru/security/For/developers/rich-formats).

### Защитные меры
Не забываем указывать параметр parser и задать custom DTD resolver:
\`\`\`python
from lxml import etree

class FakeDTDResolver(etree.Resolver):
    def resolve(self, url, id, context):
        return self.resolve_string('', context)

parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False, no_network=True)
parser.resolvers.add( FakeDTDResolver() )
xml = etree.fromstring(data, parser)
\`\`\`

Рекомендуем использовать [defusedxml](https://h.yandex-team.ru/?http%3A%2F%2Fblog.python.org%2F2013%2F02%2Fannouncing-defusedxml-fixes-for-xml.html).
`,
        "prev": "",
        "next": "python_sqli"
    },
    "python_sqli": {
        "code": `import sqlite3


def search_articles(conn, title, order_by='ASC'):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM article WHERE title LIKE '%s%%' ORDER BY title %s" % (title, order_by))
    return cursor.fetchall()`,
"md": `## Атака SQL-инъекция
SQL-инъекция — тип атаки на веб-приложение, заключающийся во внедрении SQL-выражения злоумышленника в SQL-запрос генерируемый приложением. Целью атаки являются данные пользователей, ресурсы сервера, повышение привилегий на сервере.

#### Защитные меры
**Никакой пользовательский ввод не должен попадать в SQL запросы в сыром виде**. Лучше через ORM. Если кастомные запросы все же необходимы для оптимизации, то передаём данные только строго приведенными к нужному типу и с использованием параметризированных запросов (англ. «prepared statements»).

**НЕ так**:
\`\`\`python
cursor = connection.cursor()
cursor.execute('''select something from table where param='%s';''' 
    % param)
return cursor.fetchall()
\`\`\`

**Не так**:
\`\`\`python
cursor = connection.cursor()
cursor.execute('''select''' + somethingFromUserInput + \\
    '''from''' + tableNameFromUserInput + '''where param='%s';''' 
    % param)
return cursor.fetchall()
\`\`\`

**Так**:
\`\`\`python
cursor = connection.cursor()
cursor.execute('''select something from table where param=?;''', 
    param)
return cursor.fetchall()  
\`\`\`
`,
        "prev": "python_xxe",
        "next": ""
    }
}

export default lesson;