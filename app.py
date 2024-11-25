from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE = 'employees.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Create table if not exists
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            projects TEXT NOT NULL,
            leaves INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Save employee details
@app.route('/save', methods=['POST'])
def save_employee():
    data = request.json
    name = data['name']
    role = data['role']
    projects = data['projects']
    leaves = data['leaves']
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, role, projects, leaves)
        VALUES (?, ?, ?, ?)
    ''', (name, role, projects, leaves))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Employee saved successfully!'})

# Retrieve all employees
@app.route('/retrieve', methods=['GET'])
def retrieve_employees():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    conn.close()

    result = [
        {
            'id': emp[0],
            'name': emp[1],
            'role': emp[2],
            'projects': emp[3],
            'leaves': emp[4]
        }
        for emp in employees
    ]
    return jsonify(result)

# Retrieve details about an employee by name
@app.route('/query', methods=['POST'])
def query_employee():
    name = request.json.get('name')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + name + '%',))
    employee = cursor.fetchone()
    conn.close()

    if employee:
        response = {
            'name': employee[1],
            'role': employee[2],
            'projects': employee[3],
            'leaves': employee[4]
        }
        return jsonify(response)
    return jsonify({'message': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

