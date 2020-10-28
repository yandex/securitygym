## Атака "SQL-injection"

Атака типа "Injection" позволяет атакующему внедрить произвольный код через приложение в другую систему (например, при выполнении внешних программ через shell или обращении к базам данных через SQL).

SQL-инъекции возникают, когда программа формирует запросы к базе данных динамически, включая в них данные, полученные из недоверенных источников.

### Защитные меры

Никакой пользовательский ввод не должен попадать в SQL запросы в сыром виде, лучше через ORM, если custom запросы необходимы для оптимизации — только строго приведенными к нужному типу, с использованием prepared statements:
```go
customerName := r.URL.Query().Get("name")
db.Exec("UPDATE creditcards SET name=? WHERE customerId=?", customerName, 233, 90)
```

### Задание

Данный код содержит уязвимость SQL injection. Найди и исправь уязвимость, не меняя поведение программы.

### Дополнительная информация

* https://owasp.org/www-community/attacks/SQL_Injection
* https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
* https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
* https://portswigger.net/web-security/sql-injection