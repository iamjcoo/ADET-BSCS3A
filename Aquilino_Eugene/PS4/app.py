from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': '_adet',
}

# Check connection to database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('signIn.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def signIn():
    signin_error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        if conn is None:
            flash("Unable to connect to the database.", "error")
            return render_template('signIn.html', signin_error=signin_error)

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM adet_user WHERE Email = %s", (email,))
            user = cursor.fetchone()

            if user:
                if check_password_hash(user['Password'], password):
                    # Store all user details in the session
                    session['user_id'] = user['ID']
                    session['first_name'] = user['FirstName']
                    session['middle_name'] = user['MiddleName']
                    session['last_name'] = user['LastName']
                    session['cellphone_number'] = user['CellphoneNumber']
                    session['email'] = user['Email']
                    session['home_address'] = user['HomeAddress']
                    return redirect(url_for('dashboard'))
                else:
                    signin_error = "Incorrect password. Please try again."
            else:
                signin_error = "Email not found. Please sign up first."
        except RuntimeError as e:
            flash(str(e), "error")  # Display the connection error
            return render_template('signIn.html', signin_error=signin_error)
        except mysql.connector.Error as e:
            signin_error = "Error: Unable to fetch data from the database."
            print("Error executing query:", e)
        finally:
            cursor.close()
            conn.close()
    return render_template('signIn.html', signin_error=signin_error)

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    emails = []
    if request.method == 'GET':
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Email FROM adet_user")
            emails = [row['Email'] for row in cursor.fetchall()]
            print("Existing Emails:", emails)
        finally:
            cursor.close()
            conn.close()

    if request.method == 'POST':
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        num = request.form.get('num')
        email = request.form.get('email')
        address = request.form.get('address')
        password = request.form.get('password')

        if len(password) < 8:
            signup_error = "Password must be at least 8 characters long."
            return render_template('signIn.html', signup_error=signup_error, active_signup=True)


        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Email FROM adet_user WHERE Email = %s", (email,))
            existing_email = cursor.fetchone()

            if existing_email:
                signup_error= "An account with this email already exists."
                return render_template('signIn.html', signup_error=signup_error, active_signup=True)
            elif not existing_email:
                signup_error = ""
                

            # If email doesn't exist, proceed to insert new user
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO adet_user (FirstName, MiddleName, LastName, CellphoneNumber, Email, HomeAddress, Password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (fname, mname, lname, num, email, address, hashed_password)
            )

            conn.commit()
            flash("Registration successful! Please sign in.", "success")
            return redirect(url_for('signIn'))
        except mysql.connector.Error as e:
            print("Error executing query:", e)
            flash("Error: Unable to add data to the database.", "error")
            return redirect(url_for('signIn'))
        finally:
            cursor.close()
            conn.close()
    return render_template('signIn.html', active_signup=True, existing_emails=emails)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('signIn'))

    user_details = {
        'FirstName': session.get('first_name'),
        'MiddleName': session.get('middle_name'),
        'LastName': session.get('last_name'),
        'CellphoneNumber': session.get('cellphone_number'),
        'Email': session.get('email'),
        'HomeAddress': session.get('home_address')
    }

    return render_template('dashboard.html', user=user_details)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('signIn'))

@app.route('/check-email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM adet_user WHERE Email = %s", (email,))
        exists = cursor.fetchone()[0] > 0  # Check if count is greater than 0
        return {'exists': exists}  # Return a JSON response
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
