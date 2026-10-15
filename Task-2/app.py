from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_task_key'  # Required for session management

# Initialize SQLite Database
def init_db():
    with sqlite3.connect("tasks.db") as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        """)

init_db()

# Route: / (Login Page / Home)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Mock login validation
        if username == 'admin' and password == '1234':
            session['logged_in'] = True
            return redirect(url_for('tasks_page'))
        else:
            return render_template('login.html', error="Invalid username or password!")
            
    return render_template('login.html')

# Route: /tasks – GET (Protected Page)
@app.route('/tasks')
def tasks_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    with sqlite3.connect("tasks.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT id, title, status FROM tasks")
        tasks = cursor.fetchall()
        
    return render_template('tasks.html', tasks=tasks)

# Route: /add_task – POST (AJAX endpoint)
@app.route('/add_task', methods=['POST'])
def add_task():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    title = data.get('title')
    
    if not title:
        return jsonify({'success': False, 'error': 'Task title cannot be empty'}), 400
        
    with sqlite3.connect("tasks.db") as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO tasks (title, status) VALUES (?, 'Pending')", (title,))
        task_id = cursor.lastrowid
        
    return jsonify({
        'success': True, 
        'task': {
            'id': task_id,
            'title': title,
            'status': 'Pending'
        }
    })

# Route: /logout – GET
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)