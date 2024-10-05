from flask import Flask, request, redirect, url_for, render_template, session, flash
from flask_mysqldb import MySQL
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = 'adet'

mysql = MySQL(app)

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(first_name, middle_name, last_name, contact_number, email_address, address, password):
    """Helper function to create a new user."""
    hashed_password = hash_password(password)
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address, password) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, middle_name, last_name, contact_number, email_address, address, hashed_password)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        flash('An error occurred while creating the user: {}'.format(str(e)), 'danger')
    finally:
        cursor.close()

@app.route('/')
def index():
    # Always render the login page first
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adet_user WHERE email_address=%s", (username,))
        user = cursor.fetchone()
        cursor.close()

        # Check if user exists and passwords match
        if user and user[7] == hash_password(password):  # Assuming password is at index 7
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clears all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))

    username = session['username']
    conn = mysql.connection
    cursor = conn.cursor()

    # Fetch only the details of the logged-in user
    cursor.execute("SELECT * FROM adet_user WHERE email_address=%s", (username,))
    user_details = cursor.fetchone()
    cursor.close()

    # Pass the user details to the template
    return render_template('dashboard.html', user=user_details)

@app.route('/add_user', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    middle_name = request.form.get('middle_name', '')
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email_address = request.form['email_address']
    address = request.form.get('address', '')
    password = request.form['password']

    create_user(first_name, middle_name, last_name, contact_number, email_address, address, password)

    flash('User created successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')
    address = request.form.get('address')

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE adet_user SET first_name=%s, middle_name=%s, last_name=%s, contact_number=%s, email_address=%s, address=%s WHERE id=%s",
        (first_name, middle_name, last_name, contact_number, email_address, address, user_id)
    )
    conn.commit()
    cursor.close()

    flash('User updated successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('id')  # Ensure 'id' is retrieved correctly
    print(f"Deleting user with ID: {user_id}")  # Debugging line

    if not user_id:
        flash("User ID is missing", "danger")
        return redirect(url_for('dashboard'))

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM adet_user WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()

    flash("User deleted successfully!", "success")
    return redirect(url_for('login'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form.get('address', '')
        password = request.form['password']

        create_user(first_name, middle_name, last_name, contact_number, email_address, address, password)

        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
