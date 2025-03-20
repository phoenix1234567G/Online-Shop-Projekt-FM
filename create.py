import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Tabelle für Bücher erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    condition TEXT NOT NULL
)
""")

connection.commit()
connection.close()