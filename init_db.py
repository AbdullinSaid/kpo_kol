import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO books (name, author, genre, price, number) VALUES (?, ?, ?, ?, ?)",
            ('Crime and punishment', 'Dostoevsky', 'novel', 500, 5)
            )


cur.execute("INSERT INTO books (name, author, genre, price, number) VALUES (?, ?, ?, ?, ?)",
            ('War and peace', 'Tolstoy', 'novel', 300, 7)
            )


cur.execute("INSERT INTO books (name, author, genre, price, number) VALUES (?, ?, ?, ?, ?)",
            ('The first scientific history of the War of 1812', 'Ponasenkov', 'monograph', 10000, 2)
            )

connection.commit()
connection.close()