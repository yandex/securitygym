DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS payment;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    balance INTEGER
);

CREATE TABLE payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (from_user_id) REFERENCES user (id),
    FOREIGN KEY (to_user_id) REFERENCES user (id)
);
