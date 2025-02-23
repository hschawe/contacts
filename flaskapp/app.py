"""
Help me write a flask app with a sqlite database. It should have one webpage, in pure javascript/html/css, that can load data from the sqlite database into the page, and interact with the items in the sqlite database if a button on the page is clicked.
"""

from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    count INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/update_item', methods=['POST'])
def update_item():
    data = request.json
    item_id = data.get('id')
    conn = get_db_connection()
    conn.execute('UPDATE items SET count = count + 1 WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)