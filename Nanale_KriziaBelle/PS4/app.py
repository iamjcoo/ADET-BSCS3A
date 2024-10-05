from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret_key'  # for flashing messages

# Database configuration dictionary
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

# Function to get a connection to the MySQL database
def get_connection():
    return mysql.connector.connect(**db_config)

# This route is for the home page.
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route that handles both GET and POST requests for the '/login' URL.
@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = None
    connect = None
    
    if request.method == 'POST':
        email = request.form.get('Email').strip()
        password = request.form.get('Password').strip()

        # Hash the password using SHA-256 for secure storage
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Detect whether login or signup
        action = request.form.get('action')  

        try:
            # Establish a database connection
            connect = get_connection()
            cursor = connect.cursor()

            if action == 'login':
                # Handle Login functionality
                query = "SELECT  id, first_name, password, registration_completed FROM adet_user WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()

                if user:
                    # Get the stored password
                    stored_password = user[2]  
                    registration_completed = user[3]  # Check if registration is completed

                    # Verify the stored password against the hashed input password
                    if stored_password == hashed_password:
                        session['user_id'] = user[0]  # Store user id in session
                        session['first_name'] = user[1]  # Store first name in session
                        flash('Login successful!', 'success')

                        if registration_completed:
                            return redirect(url_for('dashboard'))  # Redirect to dashboard if registration completed
                        else:
                            return redirect(url_for('index'))  # Redirect to registration form if not completed
                    else:
                        flash('Incorrect password. Please try again.', 'error')
                        return redirect(url_for('login'))
                else:
                    flash('Account does not exist. Please sign up first.', 'error')
                    return redirect(url_for('login'))

            elif action == 'signup':
                # Handle Sign Up functionality
                query = "SELECT id FROM adet_user WHERE email = %s"
                cursor.execute(query, (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # If user already exists, flash an error message
                    flash('Account with this email already exists. Please log in.', 'error')
                    return redirect(url_for('login'))
                else:
                    # Create new user since the email is not in use
                    query = "INSERT INTO adet_user (email, password, registration_completed) VALUES (%s, %s, %s)"
                    cursor.execute(query, (email, hashed_password, False))  # Set registration_completed to False initially
                    connect.commit()
                    session['user_id'] = cursor.lastrowid  # Store user id in session
                    session['first_name'] = email.split('@')[0]  # Store first name in session
                    flash('Account created successfully! Please complete the registration form.', 'success')
                    return redirect(url_for('index'))  # Redirect to the registration form

        except mysql.connector.Error as error:
            flash(f'Error, Something went wrong: {error}', 'error')
            return redirect(url_for('login'))

        finally:
            # Ensure all results are fetched before closing cursor and connection
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    return render_template('login.html')

# Route that handles the '/index' URL and supports both GET and POST methods.
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

        # Basic validation to ensure that all required fields are filled
        if not first_name or not last_name or not contact_number or not email:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))

        # Insert data into the MySQL database (based on user_id)
        try:
            connect = get_connection()
            cursor = connect.cursor()

            # SQL query to insert form data into the database for the current user_id
            query = """
                UPDATE adet_user
                SET first_name = %s, middle_name = %s, last_name = %s, contact_number = %s, address = %s, email = %s, registration_completed = %s
                WHERE id = %s
            """
            values = (first_name, middle_name, last_name, contact_number, address, email, True, session['user_id'])
            cursor.execute(query, values)
            connect.commit()

            flash('Registration information updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        except mysql.connector.Error as error:
            flash(f'Error, Something went wrong: {error}', 'error')
            return redirect(url_for('index'))

        finally:
            cursor.close()
            connect.close()

    return render_template('index.html')

# This route handles the '/dashboard' URL.
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('PLease log in first.', 'error')
        return redirect(url_for('login'))

    try:
        # Establish a database connection to fetch user details
        connect = get_connection()
        cursor = connect.cursor()

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
        flash(f'Error, Something went wrong: {err}', 'error')
        return redirect(url_for('login'))

    finally:
        # Ensure the cursor and connection are closed to free resources
        cursor.close()
        connect.close()

    return render_template('dashboard.html', user=user_details)

# Route for the success page (after successful form submission)
@app.route('/success')
def success():
    return render_template('success.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)