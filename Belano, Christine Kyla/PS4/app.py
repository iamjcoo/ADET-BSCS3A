from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key'  # for flashing messages

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def get_connection():
    return mysql.connector.connect(**config)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email').strip()
        password = request.form.get('Password').strip()

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        action = request.form.get('action')  # Detect whether login or signup

        try:
            conn = get_connection()
            cursor = conn.cursor()

            if action == 'login':
                # Handle Login
                query = "SELECT  id, first_name, password, registration_completed FROM adet_user WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()

                if user:
                    stored_password = user[2]  # Get the stored password
                    registration_completed = user[3]  # Check if registration is completed

                    if stored_password == hashed_password:
                        session['user_id'] = user[0]  # Store user id in session
                        session['first_name'] = user[1]  # Store first name in session
                        flash('Login successful!', 'success')

                        if registration_completed:
                            return redirect(url_for('dashboard'))  # Redirect to dashboard if registration completed
                        else:
                            return redirect(url_for('index'))  # Redirect to registration form if not completed
                    else:
                        flash('Invalid password', 'error')
                        return redirect(url_for('login'))
                else:
                    flash('This account does not exist. Please sign up first.', 'error')
                    return redirect(url_for('login'))

            elif action == 'signup':
                # Handle Sign Up
                query = "SELECT id FROM adet_user WHERE email = %s"
                cursor.execute(query, (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash('An account with this email already exists. Please log in.', 'error')
                    return redirect(url_for('login'))
                else:
                    # Create new user
                    query = "INSERT INTO adet_user (email, password, registration_completed) VALUES (%s, %s, %s)"
                    cursor.execute(query, (email, hashed_password, False))  # Set registration_completed to False initially
                    conn.commit()
                    session['user_id'] = cursor.lastrowid  # Store user id in session
                    session['first_name'] = email.split('@')[0]  # Store first name in session
                    flash('Account created successfully! Please complete the registration form.', 'success')
                    return redirect(url_for('index'))  # Redirect to the registration form

        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
            return redirect(url_for('login'))

        finally:
            # Ensure all results are fetched before closing cursor and connection
            if cursor:
                cursor.fetchall()  # This ensures all remaining results are fetched
                cursor.close()
            if conn:
                conn.close()

    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        flash('Please log in to access the registration form.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('First_Name').strip()
        middle_name = request.form.get('Middle_Name').strip()
        last_name = request.form.get('Last_Name').strip()
        contact_number = request.form.get('Contact_Number').strip()
        address = request.form.get('Address').strip()
        email = request.form.get('Email').strip()

        # Basic validation
        if not first_name or not last_name or not contact_number or not email:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))

        # Update data into database (based on user_id)
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Update user information in the database for the current user_id
            query = """
                UPDATE adet_user
                SET first_name = %s, middle_name = %s, last_name = %s, contact_number = %s, address = %s, email = %s, registration_completed = %s
                WHERE id = %s
            """
            values = (first_name, middle_name, last_name, contact_number, address, email, True, session['user_id'])
            cursor.execute(query, values)
            conn.commit()

            flash('Registration information updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
            return redirect(url_for('index'))

        finally:
            cursor.close()
            conn.close()

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch user details based on session['user_id']
        query = """
            SELECT first_name, middle_name, last_name, contact_number, address, email
            FROM adet_user
            WHERE id = %s
        """
        cursor.execute(query, (session['user_id'],))
        user_details = cursor.fetchone()

        if not user_details:
            flash('User details not found.', 'error')
            return redirect(url_for('login'))

    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
        return redirect(url_for('login'))

    finally:
        cursor.close()
        conn.close()

    return render_template('dashboard.html', user=user_details)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)