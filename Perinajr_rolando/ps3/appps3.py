import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Default username for XAMPP
        password='',  # Default password is empty
        database='adet'
    )
    return connection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    contact = request.form['contact']
    email = request.form['email']
    address = request.form['address']

    # Insert data into the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO adet_user (first_name, middle_name, last_name, contact, email, address)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (first_name, middle_name, last_name, contact, email, address))
    
    connection.commit()
    cursor.close()
    connection.close()

    return "Registration successful!"

if __name__ == '__main__':
    app.run(debug=True)
