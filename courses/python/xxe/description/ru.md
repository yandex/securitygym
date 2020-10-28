## Атака "XML External Entity (XXE)"

**XML External Entity (XXE)** - это тип атаки на приложение, обрабатывающее XML. Атака возможна, когда XML-парсер сконфигурирован с поддержкой внешних XML-сущностей.
XXE может привести к раскрытию конфиденциальной информации, отказу в обслуживании сервиса, SSRF (server side request forgery) и другим проблемам безопасности.

Перед использование XML-парсера для недоверенных данных:
- проверьте возможность подключения ```DTD-схем``` или ```External Entities```;
- если данная возможность включена, **явно выключите её**;
- обратите внимание на аналогичные риски при работе с документами в rich-форматах (DOCX, XLSX, PPTX и другие).

В таблице приведены атаки, к которым уязвимы XML-парсеры в конфигурации "по-умолчанию".

| Парсер     | DOS      | XXE     | XXE Parameter | URL Invocation | XInclude | XSLT |
|------------|----------|---------|---------------|----------------|----------|------|
| Etree      | **yes*** | no      | no            | no             | no       | no   |
| xml.sax    | **yes*** | **yes** | no            | **yes**        | no       | no   |
| pulldom    | **yes*** | **yes** | no            | **yes**        | no       | no   |
| lxml       | **yes**  | **yes** | no            | no             | no       | no   |
| defusedxml | no       | no      | no            | no             | no       | no   |
| minidom    | **yes*** | no      | no            | no             | no       | no   |
\* нет доступных вариантов защиты

## Защитные меры

* Рекомендуется использовать [defusedxml](https://blog.python.org/2013/02/announcing-defusedxml-fixes-for-xml.html)
* Для lxml необходимо отключить возможность процессинга xml-сущностей в текстовые значение (_resolve_entities=False_), запретить походы по сети (_no_network=True_), задать custom DTD resolver:
    ```python
    from lxml import etree

    class FakeDTDResolver(etree.Resolver):
        def resolve(self, url, id, context):
            return self.resolve_string('', context)

    parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False, no_network=True)
    parser.resolvers.add( FakeDTDResolver() )
    xml = etree.fromstring(data, parser)
    ```

### Задание

Приведенный код, обработки счетов в XML-формате, уязвим к атаке XXE. Исправь уязвимость, не меняя поведение программы.

### Дополнительная информация

* https://www.owasp.org/index.php/XML_External_Entity_%28XXE%29_Processing
* https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html