from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Set a secret key for sessions

# Database configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ADET'
}

def connect_db():
    conn = mysql.connector.connect(**config)
    return conn

# Route for index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

# Route for handling registration form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')
    password = request.form.get('password')

    # Hash the password using SHA-256 encryption
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    form_data = {
        'First_Name': first_name,
        'Middle_Name': middle_name,
        'Last_Name': last_name,
        'Contact_Number': contact_number,
        'Email_Address': email_address,
        'Password': hashed_password
    }

    # Insert the form data into the database
    conn = connect_db()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO ADET_user (first_name, middle_name, last_name, contact_number, email_address, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (first_name, middle_name, last_name, contact_number, email_address, hashed_password))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Registration successful!", "data": form_data})

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')

        # Hash the password to match the stored hash
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM ADET_user WHERE email_address = %s AND password = %s", (email_address, hashed_password))
        user = cursor.fetchone()

        if user:
            # Set session variables
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']

            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password!"

    return render_template('login.html')

# Route for dashboard, accessible only if logged in
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    # Fetch user details
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT first_name, middle_name, last_name, contact_number, email_address FROM ADET_user WHERE id = %s", (session['user_id'],))
    user_details = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('dashboard.html', first_name=session['first_name'], user_details=user_details)

# Route for logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)