from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os; print(os.getcwd())
import hashlib  # For password encryption using SHA-256

app = Flask(__name__, template_folder='template')  # Corrected template path
app.secret_key = 'your_secret_key'

# Database connection (consider using environment variables)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Leave password empty
    database="adet"
)

mycursor = mydb.cursor()

@app.route('/')
def reroute():
    return redirect(url_for('login')) 


# Registration (Sign-up) route
@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form['address']
        password = request.form['password']

        # Encrypt the password using SHA-256
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # Check if email already exists
            mycursor = mydb.cursor()
            sql = "SELECT * FROM adet_user WHERE email_address = %s"
            mycursor.execute(sql, (email_address,))
            existing_user = mycursor.fetchone()

            if existing_user:
                # Email already exists, return an error message with the template
                return render_template('register.html', error="This email is already registered. Please use a different email.")

            # Email does not exist, proceed with registration
            sql = "INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (first_name, middle_name, last_name, contact_number, email_address, address, encrypted_password)
            mycursor.execute(sql, val)
            mydb.commit()

            return redirect(url_for('login'))  # After registration, redirect to login page

        except mysql.connector.Error as err:
            print("Error: ", err)
            return "Database error", 500
        finally:
            mycursor.close()  # Always close the cursor

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()  # Encrypting the password

        try:
            # Create a new cursor for the login operation
            mycursor = mydb.cursor()

            # Prepare the SQL query to fetch user details
            sql = "SELECT id, first_name, middle_name, last_name, contact_number, email_address, address FROM adet_user WHERE email_address = %s AND password = %s"

            # Execute the query
            mycursor.execute(sql, (email_address, encrypted_password))

            # Fetch just one result
            result = mycursor.fetchone()

            # Check if a user is found
            if result:
                session['user_id'] = result[0]  # Assuming the first column is user_id
                session['first_name'] = result[1]  # Assuming the second column is first_name
                return redirect('/dashboard')  # Redirect to the dashboard
            else:
                return "Login failed", 401  # Handle login failure if no user is found

        except mysql.connector.Error as err:
            print("Error: ", err)
            return "Database error", 500
        finally:
            mycursor.close()  # Always close the cursor

    # If the request method is GET, render the login form
    return render_template('login.html')

# Dashboard route (protected)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Fetch user details excluding the password
    sql = "SELECT first_name, middle_name, last_name, contact_number, email_address, address FROM adet_user WHERE id = %s"
    mycursor.execute(sql, (session['user_id'],))
    user_details = mycursor.fetchone()

    return render_template('dashboard.html', first_name=session['first_name'], user_details=user_details)

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session data to log the user out
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)