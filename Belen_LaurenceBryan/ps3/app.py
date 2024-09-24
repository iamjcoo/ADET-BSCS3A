from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Default MySQL username for XAMPP
    'password': '',  # Leave this blank if there is no password
    'port': '3306'   # Default MySQL port
}


DB_NAME = 'adet'
TABLE_NAME = 'adet_user'

def create_database_and_table():
    try:
        # Connect to MySQL server without specifying a database
        cnx = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = cnx.cursor()

        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created or already exists.")

        # Now connect to the newly created or existing database
        cnx.database = DB_NAME

        # Create table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            middle_name VARCHAR(50),
            last_name VARCHAR(50),
            contact_number VARCHAR(20),
            email_address VARCHAR(100),
            address TEXT
        )
        """
        cursor.execute(create_table_query)
        print(f"Table {TABLE_NAME} created or already exists.")

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password")
        else:
            print(err)

@app.route('/', methods=['GET'])
def registration_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Process the form data
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')
    address = request.form.get('address')

    # Save the data to the MySQL database
    save_to_db(first_name, middle_name, last_name, contact_number, email_address, address)

    # Redirect to a thank you page or back to the form
    return redirect(url_for('registration_form'))

def save_to_db(first_name, middle_name, last_name, contact_number, email_address, address):
    try:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_NAME
        )
        cursor = cnx.cursor()

        # Insert form data into the table
        insert_query = f"""
        INSERT INTO {TABLE_NAME} (first_name, middle_name, last_name, contact_number, email_address, address)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (first_name, middle_name, last_name, contact_number, email_address, address)
        cursor.execute(insert_query, data)

        # Commit the transaction
        cnx.commit()

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    # Ensure the database and table are created before running the app
    create_database_and_table()
    app.run(debug=True)
