from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize sqlite database"""
    conn = get_db_connection()

    # use person_id as primary key b/c we can have multiple people with the same name.
    conn.execute('''CREATE TABLE IF NOT EXISTS People (
                    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT
                    )''')

    # also let's make a separate emails table so we don't have to mess around with storing emails as csv TEXT type
    conn.execute('''CREATE TABLE IF NOT EXISTS Emails (
                    person_id INTEGER,
                    email TEXT,
                    PRIMARY KEY (person_id, email)
                    )''')
    conn.commit()

    # cursor = conn.execute('INSERT INTO People (first_name, last_name) VALUES ("John", "Smith")')
    # conn.commit()
    # cursor = conn.execute('INSERT INTO Emails (person_id, email) VALUES (2, "helen.schawe@gmail.com")')
    # conn.commit()
    # cursor = conn.execute('INSERT INTO Emails (person_id, email) VALUES (3, "johnsmith@gmail.com")')
    # conn.commit()
    # s = cursor.fetchall()
    # print(s[0][0])
    # conn.commit()

    conn.close()


# CRUD operations for People
@app.route('/people', methods=['GET'])
def get_people():
    conn = get_db_connection()
    people = conn.execute('SELECT * FROM People').fetchall()
    conn.close()
    return jsonify([dict(person) for person in people])


@app.route('/people', methods=['POST'])
def add_person():
    data = request.json
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO People (first_name, last_name) VALUES (?, ?) RETURNING person_id', (data['first_name'], data['last_name']))
    s = cursor.fetchall()
    conn.close()
    return jsonify({'status': 'success', 'created_id': s[0]})


@app.route('/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE People SET first_name = ?, last_name = ? WHERE person_id = ?', (data['first_name'], data['last_name'], person_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


@app.route('/people/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM People WHERE person_id = ?', (person_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


# CRUD operations for Emails
@app.route('/emails/<int:person_id>', methods=['GET'])
def get_emails(person_id):
    conn = get_db_connection()
    emails = conn.execute('SELECT * FROM Emails WHERE person_id = ?', (person_id,)).fetchall()
    conn.close()
    return jsonify([dict(email) for email in emails])


@app.route('/emails', methods=['POST'])
def add_email():
    data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO Emails (person_id, email) VALUES (?, ?)', (data['person_id'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


@app.route('/emails', methods=['DELETE'])
def delete_email():
    data = request.json
    conn = get_db_connection()
    conn.execute('DELETE FROM Emails WHERE person_id = ? AND email = ?', (data['person_id'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


@app.route('/')
def index():

    return render_template('index.html')



if __name__ == '__main__':
    init_db()
    app.run(debug=True)