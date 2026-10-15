
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect():
    return sqlite3.connect("users.db")

with connect() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def save_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    try:
        with connect() as con:
            con.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
        return redirect('/success')
    except sqlite3.IntegrityError:
        return "Email already registered!"

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with connect() as con:
            user = con.execute(
                "SELECT name, email FROM users WHERE email=? AND password=?",
                (email, password)
            ).fetchone()

        if user:
            return render_template(
                'profile.html', name=user[0], email=user[1]
            )
        return "Invalid email or password!"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
