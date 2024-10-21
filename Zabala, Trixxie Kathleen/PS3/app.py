from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection details
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='adet',  # Replace with your MySQL database name
            user='root',     # Replace with your MySQL username
            password=''  # Replace with your MySQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Create table if it doesn't exist
def create_table():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adet_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                middlename VARCHAR(255),
                lastname VARCHAR(255),
                contact VARCHAR(50),
                email VARCHAR(255) UNIQUE,
                address VARCHAR(255)
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()

@app.route('/')
def index():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['firstname']
    middlename = request.form['middlename']
    lastname = request.form['lastname']
    contact = request.form['contact']
    email = request.form['email']
    address = request.form['address']

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # Check if the email already exists
        cursor.execute("SELECT * FROM adet_users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'message': 'Email already exists!'}), 400

        # Insert new user data into MySQL
        cursor.execute('''
            INSERT INTO adet_users (firstname, middlename, lastname, contact, email, address) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (firstname, middlename, lastname, contact, email, address))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Registration successful!'}), 201
    else:
        return jsonify({'message': 'Database connection failed!'}), 500

if __name__ == '__main__':
    create_table()  # Ensure the table exists before running the app
    app.run(debug=True)
