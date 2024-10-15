from flask import Flask, request, render_template, redirect, url_for, flash, session
from mysql.connector import Error
import mysql.connector
import re
import hashlib
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = Config.get_db_config()

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def log_user_data_to_sql_file(data):
    sql_file = 'user_data.sql'
    sql_entry = f"INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address) VALUES " \
                f"('{data['first_name']}', '{data['middle_name']}', '{data['last_name']}', '{data['contact_number']}', " \
                f"'{data['email_address']}', '{data['address']}');\n"
    
    with open(sql_file, 'a') as f:
        f.write(sql_entry)
        
def log_saved_data_to_sql_file(password):
    sql_file = 'saved_data.sql'
    sql_entry = f"INSERT INTO login_history (password, login_time) VALUES ('{password}', NOW());\n"
    
    with open(sql_file, 'a') as f:
        f.write(sql_entry)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        middle_name = request.form.get('middlename')
        last_name = request.form.get('lastname')
        contact_number = request.form.get('contact')
        email_address = request.form.get('email')
        address = request.form.get('address')
        password = request.form.get('password')

        # Validation
        if not first_name or not last_name or not contact_number or not email_address or not password:
            flash("Error: All fields are required.", 'error')
            return redirect(url_for('signup'))
        
        if not is_valid_email(email_address):
            flash("Error: Invalid email format.", 'error')
            return redirect(url_for('signup'))

        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Check if email already exists
            cursor.execute("SELECT COUNT(*) FROM adet_user WHERE password = %s", (password,))
            count = cursor.fetchone()[0]

            if count > 0:
                flash("Error: Email address already registered.", 'error')
                return redirect(url_for('signup'))

            # Insert data
            insert_query = """
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (first_name, middle_name, last_name, contact_number, email_address, address, generate_password_hash(password)))
            connection.commit()

            log_user_data_to_sql_file({
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'contact_number': contact_number,
                'email_address': email_address,
                'address': address
            })
            flash("Registration successful!", 'success')
            return redirect(url_for('login'))

        except Error as e:
            error_message = f"Error while inserting data: {e}"
            print(error_message)
            flash(error_message, 'error')
            return redirect(url_for('signup'))

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form.get('email')
        password = request.form.get('password')

        if not email_address or not password:
            flash("Error: Email and password are required.", 'error')
            return redirect(url_for('login'))

        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            cursor.execute("SELECT first_name, password FROM adet_user WHERE email_address = %s", 
                           (email_address,))
            user = cursor.fetchone()

            if user:
                if check_password_hash(user[1], password):
                    session['first_name'] = user[0]
                    session['email_address'] = email_address
                    flash("Login successful!", 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash("Error: Invalid email or password.", 'error')
            else:
                flash("Error: Invalid email or password.", 'error')

            return redirect(url_for('login'))

        except Error as e:
            flash(f"Error while accessing data: {e}", 'error')
            return redirect(url_for('login'))

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'email_address' not in session:
        flash("Please log in first.", 'error')
        return redirect(url_for('login'))

    connection = None
    cursor = None
    user_details = {}
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, middle_name, last_name, contact_number, email_address, address FROM adet_user WHERE email_address = %s", 
                       (session['email_address'],))
        user_details = cursor.fetchone()

    except Error as e:
        print(f"Error while fetching user details: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    # Read user_data.txt file to display its contents
    user_data_content = ""
    if os.path.exists('user_data.txt'):
        with open('user_data.txt', 'r') as file:
            user_data_content = file.read()

    return render_template('dashboard.html', first_name=session['first_name'], user_details=user_details, user_data_content=user_data_content)

@app.route('/logout')
def logout():
    session.pop('first_name', None)
    session.pop('email_address', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
