#http://127.0.0.1:5000/c for signup
#http://127.0.0.1:5000/login for login

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def get_db_connection():
    """Establish a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/c', methods=['GET', 'POST']) 
def signup():
    if request.method == 'POST':
        first_name = request.form['first-name']
        middle_initial = request.form['middle-initial']
        last_name = request.form['last-name']
        address = request.form['address']
        email_address = request.form['email-address']
        contact_number = request.form['contact-number']
        password_signup = request.form['password-signup']

        hashed_password = hashlib.sha256(password_signup.encode()).hexdigest()

        conn = get_db_connection()
        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor()

        try:
            insert_query = '''
                INSERT INTO adet_user (first_name, middle_initial, last_name, address, email_address, contact_number, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (first_name, middle_initial, last_name, address, email_address, contact_number, hashed_password))
            conn.commit()

            welcome_message = f"Hello {first_name}, Welcome to CCS 106 - Applications Development and Emerging Technologies!"
            return redirect(url_for('welcome', message=welcome_message))

        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data into the database", 500
        finally:
            cursor.close()
            conn.close()

    return render_template('c.html')  

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email_address = request.form.get('email-address')
        password = request.form.get('password')

   
        if not email_address or not password:
            flash('Email and password are required.')
            return redirect(url_for('login'))

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor()

        try:
            select_query = '''
                SELECT first_name FROM adet_user 
                WHERE email_address = %s AND password = %s
            '''
            cursor.execute(select_query, (email_address, hashed_password))

            user = cursor.fetchone()

            if user:
                welcome_message = f"Hello {user[0]}, Welcome back to CCS 106 Applications Development and Emerging Technologies!"
                return render_template('welcome.html', message=welcome_message)
            else:
                flash('Invalid email or password. Please try again.')
                return redirect(url_for('login'))

        except mysql.connector.Error as e:
            print(f"Error during login: {e}")
            return "Error during login", 500
        finally:
            cursor.fetchall()  # Clear any unread results (optional safeguard)
            cursor.close()
            conn.close()

    return render_template('login.html')  # Render login page for GET request

@app.route('/welcome')  
def welcome():
    message = request.args.get('message')
    return render_template('welcome.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
