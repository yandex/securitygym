## Insecure Direct Object Reference

Insecure Direct Object Reference (Небезопасная прямая ссылка на объект, IDOR) возникает, когда приложения явно использует имя или ключ объекта при генерации веб-страниц, не проверяя при этом права пользователя при запросе им объекта.

Для эксплуатации злоумышленнику достаточно изменить значение параметра, ссылающегося на объект, на такое, чтобы ссылка была на объект, к которому у пользователя доступа нет.

### Защитные меры

Проверяем для каждого запроса, что пользователь авторизован на доступ к объекту.

### Задание

Данный код содержит IDOR в одном из методов. Найди и исправь уязвимость, не меняя поведение программы.
Все платежи хранятся в таблице payment:
```sql
CREATE TABLE payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- идентификатор платежа
    user_id INTEGER NOT NULL, -- идентификатор пользователя, который сделал платеж
    amount DECIMAL(10,2) NOT NULL, -- количество переведенных средств
    description TEXT, -- комментарий к платежу
    FOREIGN KEY (user_id) REFERENCES user (id)
);
```

### Дополнительная информация

* https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
* https://portswigger.net/web-security/access-control/idor