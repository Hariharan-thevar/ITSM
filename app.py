from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            issue TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        name = request.form['name']
        issue = request.form['issue']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tickets (name, issue, status) VALUES (?, ?, ?)", 
                       (name, issue, "Open"))
        conn.commit()
        conn.close()
        return redirect('/tickets')
    return render_template('create_ticket.html')

@app.route('/tickets')
def view_tickets():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()
    return render_template('view_tickets.html', tickets=tickets)

@app.route('/close/<int:id>')
def close_ticket(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status='Closed' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/tickets')

if __name__ == '__main__':
    app.run(debug=True)
