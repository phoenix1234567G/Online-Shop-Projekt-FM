from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = 'geheime_schluessel'  # In der Produktion sollte ein sicherer Schlüssel verwendet werden
bcrypt = Bcrypt(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Damit Zeilen als Dictionary-ähnliche Objekte abgerufen werden können
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, category FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products, user=session.get('user'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Die Passwörter stimmen nicht überein.")
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            flash("Registrierung erfolgreich. Bitte loggen Sie sich ein.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Fehler: Benutzername bereits vergeben.")
            conn.close()
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = username
            flash("Erfolgreich eingeloggt.")
            return redirect(url_for('index'))
        else:
            flash("Fehler: Falscher Benutzername oder Passwort.")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Sie wurden ausgeloggt.")
    return redirect(url_for('index'))

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user' not in session:
        flash("Bitte loggen Sie sich ein, um ein Produkt hinzuzufügen.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)", (name, price, category))
        conn.commit()
        conn.close()

        flash("Produkt wurde erfolgreich hinzugefügt.")
        return redirect(url_for('index'))
    return render_template('add_item.html', user=session.get('user'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, category FROM products WHERE name LIKE ?", ('%' + query + '%',))
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products, user=session.get('user'))

if __name__ == '__main__':
    app.run(debug=True)