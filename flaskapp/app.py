from typing import List
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

    # cursor = conn.execute('INSERT INTO People (first_name, last_name) VALUES ("Helen", "Schawe") RETURNING person_id')
    # s = cursor.fetchall()
    # conn.commit()
    # cursor = conn.execute(f'INSERT INTO Emails (person_id, email) VALUES ({s[0][0]}, "helen.schawe@gmail.com")')
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


# CRUD operations for Emails
@app.route('/emails/<int:person_id>', methods=['GET'])
def get_emails(person_id):
    conn = get_db_connection()
    emails = conn.execute('SELECT * FROM Emails WHERE person_id = ?', (person_id,)).fetchall()
    conn.close()
    return jsonify([dict(email) for email in emails])


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['DELETE'])
def form_handle_delete():
    # Get request data
    input_data = request.json
    print("DELETE:", input_data)
    person_id = input_data['person_id']

    # Execute deletes from both emails and people tables
    conn = get_db_connection()
    conn.execute('DELETE FROM People WHERE person_id = ?', (person_id,))
    conn.commit()

    conn.execute('DELETE FROM Emails WHERE person_id = ?', (person_id,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})


@app.route('/', methods=['POST'])
def form_handle_save():
    # Get form input data
    form_data = request.form
    print(form_data)
    form_person_id = form_data.get('person_id', "")
    print(form_person_id)
    conn = get_db_connection()
    if form_person_id == "":
        # If no person_id was passed, this is a new contact
        conn = get_db_connection()

        cursor = conn.execute('INSERT INTO People (first_name, last_name) VALUES (?, ?) RETURNING person_id',
                              (form_data['first_name'], form_data['last_name']))
        s = cursor.fetchall()
        new_person_id = s[0][0]
        conn.commit()
        conn.close()

        # Also add emails if they are present
        insert_emails(new_person_id, form_data.getlist("inputs[]"))
    else:
        conn.execute('UPDATE People SET first_name = ?, last_name = ? WHERE person_id = ?',
                     (form_data.get('first_name'), form_data.get('last_name'), form_person_id,))
        conn.commit()

        # Delete and recreate emails in Emails table
        conn.execute('DELETE FROM Emails WHERE person_id = ?', (form_person_id,))
        conn.commit()
        conn.close()

        # Now insert all the emails given as if they were new
        insert_emails(form_person_id, form_data.getlist("inputs[]"))

    print('done')
    return jsonify({'status': 'success'})


def insert_emails(person_id: int, form_emails: List = None):
    conn = get_db_connection()
    if form_emails:
        insert_sql = 'INSERT INTO Emails (person_id, email) VALUES'
        for email in form_emails:
            insert_sql += f' ({person_id}, "{email}"),'
        insert_sql = insert_sql.rstrip(",")
        conn.execute(insert_sql)
        conn.commit()
    conn.close()



if __name__ == '__main__':
    init_db()
    app.run(debug=True)