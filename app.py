from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = 'geheime_schluessel'  # Für Sessions erforderlich
bcrypt = Bcrypt(app)

# Startseite mit Bücherliste
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, price, condition FROM books")
    books = cursor.fetchall()
    conn.close()

    return render_template('index.html', books=books, user=session.get('user'))

# Registrierung neuer Benutzer
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Fehler: Benutzername bereits vergeben."

    return render_template('register.html')

# Benutzer-Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[0], password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "Fehler: Falscher Benutzername oder Passwort."

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Nur angemeldete Nutzer können Bücher hinzufügen
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        condition = request.form['condition']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, price, condition) VALUES (?, ?, ?)", (title, price, condition))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_book.html', user=session.get('user'))

# Flask-Server starten
if __name__ == '__main__':
    app.run(debug=True)