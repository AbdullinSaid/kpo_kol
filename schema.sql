DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    price INTEGER NOT NULL,
    number INTEGER NOT NULL
);