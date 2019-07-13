DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    created_at DATETIME NOT NULL
);

INSERT INTO messages (message, created_at) VALUES ('Hello, world! This is guestbook!', '2019-05-23 09:15:00');
