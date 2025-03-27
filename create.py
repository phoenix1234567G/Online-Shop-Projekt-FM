import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Tabelle für Benutzer erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Benutzertabelle erfolgreich erstellt!")