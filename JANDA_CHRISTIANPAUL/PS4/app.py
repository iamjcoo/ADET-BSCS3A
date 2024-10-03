from os import access
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector as mc
from mysql.connector import errorcode
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
try:
    mydb = mc.connect(
        host='localhost',
        user='root',
        database='users'
    )
    mycursor = mydb.cursor(buffered=True)
except mc.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        mydb = mc.connect(
            host='localhost',
            user='root'
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE users")
        mycursor.execute("USE users")
        mycursor.execute(
            "CREATE TABLE accounts ("
            "   first_name VARCHAR(255) NOT NULL,"
            "   middle_name VARCHAR(255) DEFAULT NULL,"
            "   last_name VARCHAR(255) NOT NULL,"
            "   contact_number VARCHAR(11) NOT NULL,"
            "   email VARCHAR(255) NOT NULL UNIQUE,"
            "   address TEXT NOT NULL,"
            "   password VARCHAR(255) NOT NULL"
            ")"
        )
    else:
        raise

# Route for rendering the registration form
@app.route('/')
def registration_form():
    return render_template('form.html')

# Route for handling form submission and saving to MySQL
@app.route('/submit', methods=['POST'])
def register():
    first_name = request.form['firstName']
    middle_name = request.form.get('middleName', '')
    last_name = request.form['lastName']
    contact_number = request.form['contactNumber']
    email = request.form['email']
    address = request.form['address']
    password = request.form['password']

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Insert user data into the database
    query = "INSERT INTO accounts (first_name, middle_name, last_name, contact_number, email, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (first_name, middle_name, last_name, contact_number, email, address, hashed_password)
    
    try:
        mycursor.execute(query, val)
        mydb.commit()
        return jsonify(message="Registration successful!")
    except mc.Error as e:
        return jsonify(message="Error: {}".format(e))

# Route for rendering the login page
@app.route('/login_page')
def login_page():
    return render_template('login.html')

# Route for handling login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Hash the input password to compare with stored hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check user credentials
    query = "SELECT first_name, middle_name, last_name, contact_number, email, address, HEX(password) FROM accounts WHERE email = %s"
    mycursor.execute(query, (username,))
    user_data = mycursor.fetchone()

    if user_data != None and user_data[-1] == hashed_password.upper():
        # Store user data in session
        session['user'] = {
            'first_name': user_data[0],
            'middle_name': user_data[1],
            'last_name': user_data[2],
            'contact_number': user_data[3],
            'email': user_data[4],
            'address': user_data[5]
        }
         # On success, return a success message
        return jsonify(success=True, message="Login successful!")
    
     # If credentials are invalid, return a failure message
    return jsonify(success=False, message="Invalid username or password.")

# Route for rendering the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login_page'))

    return render_template('dashboard.html', user=session['user'])

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
