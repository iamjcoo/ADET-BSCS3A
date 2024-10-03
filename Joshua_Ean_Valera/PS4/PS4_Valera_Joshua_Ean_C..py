from flask import Flask, render_template, request, redirect, flash, session
import db
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db.init_app(app)

@app.route('/')
def index():
    # Check if there are registered users
    if db.get_all_users():  # This will return a list of users
        return redirect('/login')
    else:
        flash("No registered accounts. Please register first.", "danger")
        return redirect('/login')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the entered password using sha256
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        # Retrieve user details from the database
        user = db.get_user_by_email(email)

        # Compare the hashed password with the stored hash
        if user and user[5] == encrypted_password:  # Assuming the password is the 5th field in the user tuple
            session['user_id'] = user[0]  # Store user ID in session
            session['first_name'] = user[1]  # Store first name for welcome message
            flash(f"Welcome, {user[1]}!", 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

# Registration Form Route
@app.route('/register', methods=['GET', 'POST'])
def registration_form():
    if request.method == 'POST':
        first_name = request.form.get('validationDefault01')
        middle_name = request.form.get('validationDefault02')
        last_name = request.form.get('validationDefault03')
        email = request.form.get('inputEmail4')
        password = request.form.get('inputPassword4')
        address = request.form.get('inputAddress')
        contact_number = request.form.get('inputContact')

        # Hash the password using sha256
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            db.add_user(first_name, middle_name, last_name, email, encrypted_password, address, contact_number)
            flash('User successfully registered', 'success')
            return redirect('/login')
        except Exception as e:
            print(f"Error during user registration: {str(e)}")
            flash(f"Error during registration: {str(e)}", 'danger')
            return redirect('/register')

    return render_template('registration.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must log in to access the dashboard', 'danger')
        return redirect('/login')

    user_details = db.get_user_by_id(session['user_id'])
    return render_template('dashboard.html', user=user_details)

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
