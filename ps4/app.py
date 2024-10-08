from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import errorcode
import hashlib  # Import hashlib for SHA-256 hashing

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Default MySQL username for XAMPP
    'password': '',  # Leave this blank if there is no password
    'port': '3306'   # Default MySQL port
}

DB_NAME = 'adet'
USER_TABLE_NAME = 'adet_user'

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
        CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            middle_name VARCHAR(50),
            last_name VARCHAR(50),
            contact_number VARCHAR(20),
            email VARCHAR(100) NOT NULL UNIQUE,
            address TEXT,
            password VARCHAR(64) NOT NULL  -- Length for SHA-256 hash
        )
        """
        cursor.execute(create_table_query)
        print(f"Table {USER_TABLE_NAME} created or already exists.")

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username or password")
        else:
            print(err)

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def registration_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Process the form data
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email = request.form.get('email')
    address = request.form.get('address')
    password = request.form.get('password')

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Save the data to the MySQL database
    save_to_db(first_name, middle_name, last_name, contact_number, email, address, hashed_password)

    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for('login'))  # Redirect to the login page after successful registration

def save_to_db(first_name, middle_name, last_name, contact_number, email, address, hashed_password):
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
        INSERT INTO {USER_TABLE_NAME} (first_name, middle_name, last_name, contact_number, email, address, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (first_name, middle_name, last_name, contact_number, email, address, hashed_password)
        cursor.execute(insert_query, data)

        # Commit the transaction
        cnx.commit()

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if the user exists and verify password
    user = get_user_by_email(email)
    if user:
        # Compare with stored hashed password
        if user[7] == hashed_password:  # Adjust index according to your table schema
            session['user_id'] = user[0]  # Store user ID in session
            session['first_name'] = user[1]  # Store first name in session
            session['middle_name'] = user[2]  # Store middle name in session
            session['last_name'] = user[3]  # Store last name in session
            session['contact_number'] = user[4]  # Store contact number in session
            session['email'] = user[5]  # Store email in session
            session['address'] = user[6]  # Store address in session
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for('login'))
    else:
        flash("Invalid email or password", "danger")
        return redirect(url_for('login'))

def get_user_by_email(email):
    try:
        cnx = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_NAME
        )
        cursor = cnx.cursor()

        query = f"SELECT * FROM {USER_TABLE_NAME} WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        cursor.close()
        cnx.close()
        return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', 
                               first_name=session['first_name'],
                               middle_name=session['middle_name'],
                               last_name=session['last_name'],
                               contact_number=session['contact_number'],
                               email=session['email'],
                               address=session['address'])
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Ensure the database and table are created before running the app
    create_database_and_table()
    app.run(debug=True)
