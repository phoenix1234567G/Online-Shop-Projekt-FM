import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Tabelle für Produkte erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL
)
""")

connection.commit()
connection.close()