from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Database connection details
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'adets'  # Updated database name here
}

# Function to establish connection to MySQL
def connect_to_db():
    return mysql.connector.connect(**db_config)

# Function to create the database and the user table
def setup_database():
    with connect_to_db() as conn:
        cursor = conn.cursor()

        # Create the `adets` database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS adets")
        cursor.execute("USE adets")

        # Create the `adet_user` table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS adet_user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            middle_name VARCHAR(255),
            last_name VARCHAR(255) NOT NULL,
            contact_number VARCHAR(20) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            address TEXT
        )''')

        conn.commit()

# Call the function to set up the database on app start
setup_database()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    form_data = request.form
    first_name = form_data['first_name']
    middle_name = form_data['middle_name']
    last_name = form_data['last_name']
    contact_number = form_data['contact_number']
    email = form_data['email']
    password = form_data['password']
    address = form_data['address']

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Insert user data into the database
    try:
        with connect_to_db() as conn:
            cursor = conn.cursor()
            sql = '''INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, password, address)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql, (first_name, middle_name, last_name, contact_number, email, hashed_password, address))
            conn.commit()
        flash("Registration successful! Please log in.")
    except mysql.connector.Error as error:
        flash(f"Failed to insert record: {error}")

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the input password

        with connect_to_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM adet_user WHERE email = %s AND password = %s', (email, hashed_password))
            user = cursor.fetchone()

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

    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT first_name, contact_number, email, address FROM adet_user WHERE id = %s',
            (session['user_id'],)
        )
        user_details = cursor.fetchone()

    return render_template('dashboard.html', first_name=session['first_name'], user_details=user_details)
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
