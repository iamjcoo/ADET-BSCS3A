from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

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

# Hash the password using SHA-256
def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
                username VARCHAR(255) UNIQUE,
                address VARCHAR(255),
                password_hash VARCHAR(255)
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()

# Route to the registration page
@app.route('/')
def index():
    return render_template('registration.html')

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['firstname']
    middlename = request.form['middlename']
    lastname = request.form['lastname']
    contact = request.form['contact']
    email = request.form['email']
    username = request.form['username']
    address = request.form['address']
    password = request.form['password']

    # Hash the password using SHA-256 before saving
    password_hash = sha256_hash(password)

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        # Check if the email or username already exists
        cursor.execute("SELECT * FROM adet_users WHERE email = %s OR username = %s", (email, username))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'message': 'Email or username already exists!'}), 400

        # Insert new user data into MySQL with the hashed password
        cursor.execute('''
            INSERT INTO adet_users (firstname, middlename, lastname, contact, email, username, address, password_hash) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (firstname, middlename, lastname, contact, email, username, address, password_hash))

        connection.commit()
        cursor.close()
        connection.close()

        # After successful registration, redirect to the success page
        return redirect(url_for('register_success'))
    else:
        return jsonify({'message': 'Database connection failed!'}), 500

@app.route('/register-success')
def register_success():
    return render_template('register_success.html')

# Route to display the login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    connection = get_db_connection()
    if connection is None:
        return jsonify({'message': 'Database connection failed!'}), 500

    cursor = connection.cursor()

    # Fetch the user by username
    cursor.execute("SELECT * FROM adet_users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        stored_password_hash = user[8]  # Assuming the hashed password is in column 7

        # Hash the entered password to compare with the stored hash
        entered_password_hash = sha256_hash(password)

        # Debugging: Print both the stored hash and the entered hashed password
        print(f"Entered password hash: {entered_password_hash}")
        print(f"Stored password hash: {stored_password_hash}")

        # Compare the hashed passwords
        if stored_password_hash == entered_password_hash:
            print("Password matches!")
            session['user_id'] = user[0]
            session['firstname'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            print("Password does not match!")
            return jsonify({'message': 'Invalid password!'}), 401
    else:
        print("User not found!")
        return jsonify({'message': 'Username not found!'}), 401

# Route for the Dashboard, accessible only to logged-in users
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT firstname, middlename, lastname, contact, email, username, address FROM adet_users WHERE id = %s", (session['user_id'],))
        user_details = cursor.fetchone()

        return render_template('dashboard.html', firstname=session['firstname'], user_details=user_details)

    return jsonify({'message': 'Error loading dashboard!'}), 500

# Route to handle logout
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login_page'))  # Redirect to login page after logout

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
