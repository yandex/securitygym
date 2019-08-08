CREATE TABLE IF NOT EXISTS users (
    uid SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS completed_lessons (
    uid INT NOT NULL,
    course VARCHAR(128) NOT NULL,
    lesson VARCHAR(128) NOT NULL,
    PRIMARY KEY (uid, course, lesson)
);