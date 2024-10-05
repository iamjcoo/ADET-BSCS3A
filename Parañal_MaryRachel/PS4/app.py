from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'secret'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  
        database='adet'  
    )

# Route for the home page
@app.route('/')
def index():
    return render_template('login.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']

        # Hashing the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check for duplicate account
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adet_user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Account with this email already exists. Please sign in or use a different email.', 'error')
            return render_template('signup.html')

        # Inserting new user into the database
        cursor.execute("""
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (first_name, middle_name, last_name, contact_number, email, address, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('success'))

    return render_template('signup.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adet_user WHERE email = %s AND password = %s", (email, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user[0]  
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adet_user WHERE id = %s", (user_id,))
        user_details = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template('dashboard.html', user=user_details)

    return redirect(url_for('login'))

# Route for success page
@app.route('/success')
def success():
    return render_template('success.html')

# Route to logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
