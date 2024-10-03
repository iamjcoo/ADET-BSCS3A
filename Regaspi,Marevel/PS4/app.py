from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Temporary in-memory storage for registered users
users = []

@app.route('/', methods=['GET', 'POST'])
def submit():
    errors = {}  # Initialize the errors dictionary
    user_data = {}  # Ensure user data is empty when rendering the form

    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email_address = request.form.get('email_address')
        address = request.form.get('address')
        password = request.form.get('password')

        # Basic validation
        if not first_name or not first_name[0].isupper():
            errors['first_name'] = 'First Name is required and must start with a capital letter.'
        if not middle_name or not middle_name[0].isupper():
            errors['middle_name'] = 'Middle Name must start with a capital letter.'
        if not last_name:
            errors['last_name'] = 'Last Name is required.'
        if not email_address:
            errors['email_address'] = 'Email Address is required.'
        elif '@' not in email_address:
            errors['email_address'] = 'Email address must contain @.'
        if not contact_number:
            errors['contact_number'] = 'Contact Number is required.'
        elif len(contact_number) != 11:
            errors['contact_number'] = 'Contact Number must be 11 digits long.'
        if not password:
            errors['password'] = 'Password is required.'

        # If there are validation errors, return the form data to the user
        if errors:
            user_data = request.form  # Keep the current form data in case of errors
            return render_template('form.html', errors=errors, user_data=user_data)

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save the user data into in-memory storage
        users.append({
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address,
            'password': hashed_password
        })

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    # Pass empty user data on initial load
    return render_template('form.html', errors=errors, user_data={})


@app.route('/logout')
def logout():
    # Clear the session to remove any user information
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('submit'))  # Redirect to the submit page (empty form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}  # Initialize the errors dictionary

    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Validate input
        if not email_address:
            errors['email_address'] = 'Email Address is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if errors:
            return render_template('login.html', errors=errors)

        # Authenticate the user by checking against in-memory storage
        user = next((user for user in users if user['email_address'] == email_address and user['password'] == hashed_password), None)

        if user:
            session['user_id'] = user['email_address']
            session['first_name'] = user['first_name']
            return redirect(url_for('dashboard'))
        else:
            errors['login'] = 'Invalid email or password.'
            return render_template('login.html', errors=errors)

    # Prevent caching of the login page and ensure no sensitive info is retained
    response = make_response(render_template('login.html', errors=errors))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to view the dashboard.')
        return redirect(url_for('login'))

    user = next((user for user in users if user['email_address'] == session['user_id']), None)

    if user:
        return render_template('dashboard.html', first_name=session.get('first_name'), user_details=user)
    else:
        flash('User details not found.')
        return redirect(url_for('login'))  # Redirect if user details not found

if __name__ == '__main__':
    app.run(debug=True)
