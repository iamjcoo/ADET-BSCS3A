from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Database connection details
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'adet'
}

# Function to establish connection to MySQL
def connect_with_db():
    return mysql.connector.connect(**db_config)

# Automatically create database and table if they don't exist
def create_db_and_table():
    conn = connect_with_db()
    cursor = conn.cursor()

    # Create the `adet` database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS adet")
    
    # Switch to the `adet` database
    cursor.execute("USE adet")

    # Create the `adet_user` table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS adet_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        middle_name VARCHAR(255),
        last_name VARCHAR(255) NOT NULL,
        contact_number VARCHAR(20) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,  -- Store hashed password
        address TEXT
    )''')

    conn.commit()
    cursor.close()
    conn.close()

# Call the function to create the database and table on app start
create_db_and_table()

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        password = request.form['password']  # Get password
        address = request.form['address']

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert data into MySQL database
        conn = connect_with_db()
        cursor = conn.cursor()

        sql = '''INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, password, address)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        val = (first_name, middle_name, last_name, contact_number, email, hashed_password, address)

        try:
            cursor.execute(sql, val)
            conn.commit()
            flash("Registration successful! Please log in.")
        except mysql.connector.Error as error:
            flash(f"Failed to insert record: {error}")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the input password

        conn = connect_with_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM adet_user WHERE email = %s AND password = %s', (email, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user[0]  # Store user ID in session
            session['first_name'] = user[1]  # Store first name in session
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. Please try again.")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))

    conn = connect_with_db()
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, middle_name, last_name, contact_number, email, address FROM adet_user WHERE id = %s', (session['user_id'],))
    user_details = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('dashboard.html', first_name=session['first_name'], user_details=user_details)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
