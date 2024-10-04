from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib  # Import hashlib for hashing passwords

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# MySQL connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Change this if your MySQL server is not local
        user='root',  # Enter your MySQL username
        password='',  # Enter your MySQL password
        database='adet3a'  # Name of your database
    )
    return connection

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Hash password using SHA-256

# Function to save form data to MySQL database
def save_to_database(data):
    connection = get_db_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO adet3a_users (first_name, middle_name, last_name, contact_number, email_address, address, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['contact_number'],
        data['email_address'],
        data['address'],
        data['password']  # Save the hashed password
    ))

    connection.commit()
    cursor.close()
    connection.close()

# Function to verify user credentials
def verify_user(email_address, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Hash the password before checking
    hashed_password = hash_password(password)

    query = "SELECT * FROM adet3a_users WHERE email_address = %s AND password = %s"
    cursor.execute(query, (email_address, hashed_password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user

# Route for the login form
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        
        user = verify_user(email_address, password)

        if user:
            session['user_id'] = user[0]  # Assuming the first column is user ID
            session['user_name'] = user[2]  # Assuming the third column is the user's name
            return redirect(url_for('dashboard'))
        else:
            # Check if the email exists in the database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM adet3a_users WHERE email_address = %s", (email_address,))
            existing_user = cursor.fetchone()

            cursor.close()
            connection.close()

            if existing_user:
                flash('Incorrect password. Please try again.', 'error')
            else:
                flash('No such user is registered.', 'error')  # Flash error message for non-existent user

            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form['address']
        password = request.form['password']

        # Simple validation
        if not first_name or not last_name or not contact_number or not email_address or not address or not password:
            flash("Please fill out all required fields!", 'error')
            return redirect(url_for('register'))

        # Prepare data for saving
        form_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address,
            'password': hash_password(password)  # Hash the password before saving
        }

        # Save the data to MySQL
        save_to_database(form_data)

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('register'))  # Or redirect to login page if preferred

    return render_template('register.html')


# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    
    # Get user info from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT first_name, middle_name, last_name, contact_number, email_address, address FROM adet3a_users WHERE id = %s", (user_id,))
    user_info = cursor.fetchone()  # Fetch user details
    
    cursor.close()
    connection.close()

    return render_template('dashboard.html', user_name=user_name, user_info=user_info)



@app.route('/logout')
def logout():
    # Logic to log the user out
    flash('You have been logged out.', 'error')  # Use 'error' to match the styling
    return redirect(url_for('login'))  # Redirect to the login page

if __name__ == '__main__':
    app.run(debug=True)
