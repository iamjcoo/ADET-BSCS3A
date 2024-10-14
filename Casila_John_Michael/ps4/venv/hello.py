from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import timedelta
import time
import re

app = Flask(__name__)

# Set a secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/usersDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.permanent_session_lifetime = timedelta(minutes=5)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    Fname = db.Column(db.String(20), nullable=False)
    Mname = db.Column(db.String(20), nullable=False)
    Lname = db.Column(db.String(20), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(120), nullable=False)
    Contact = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(64), nullable=False)  # Adjusted length for hashed password

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    time.sleep(1)
    return f"<h1><strong>You have been logged out</strong><h1>"


@app.route('/check', methods=['POST'])
def check_login():
    if request.method == 'POST':
        email = request.form['email']
        input_password = request.form['password']
        
        # Hash the input password
        hash_object = hashlib.sha256(input_password.encode())
        hex_dig = hash_object.hexdigest()

        # Query to check if the user exists
        user = User.query.filter_by(Email=email).first()
        if user and user.Password == hex_dig:
            # Login successful
            session['user_id'] = user.id  # Store user ID in the session
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash("Invalid email or password!", "danger")   
    return redirect(url_for('login'))  # Redirect back to login on failure



@app.route("/dashboard")
def dashboard():
    user_id = session.get('user_id')  # Get user ID from session
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user = User.query.get(user_id)  # Fetch the user from the database

    if user:
        return render_template("dashboard.html", user=user)  # Pass user data to template
    else:
        return "User not found!", 404
    
    
    
    
@app.route("/signup")
def signup():
    return render_template("signup.html")




@app.route('/save', methods=['POST'])
def save():
    # Store user data in session instead of using global variables
    session['fname'] = request.form['fname']
    session['mname'] = request.form['mname']
    session['lname'] = request.form['lname']
    session['age'] = request.form['age']
    session['address'] = request.form['address']
    session['email'] = request.form['email']
    session['contact'] = request.form['contact']
    time.sleep(1)
    # Redirect to the password input page
    return redirect(url_for('ask_password'))





@app.route('/ask_password', methods=['GET', 'POST'])
def ask_password():
    # Render password input page
    time.sleep(1)
    if request.method == 'POST':
        return redirect(url_for('save_password'))
    return render_template("password.html")  # Serve password input page



@app.route("/save_password", methods=['POST'])
def save_password():
    # Retrieve the hashed password
    password = request.form['password']
    hash_object = hashlib.sha256(password.encode())
    hex_dig = hash_object.hexdigest()

        # Create a new user with hashed password using session data
    new_user = User(
        Fname=session['fname'],
        Mname=session['mname'],
        Lname=session['lname'],
        Age=session['age'],
        Address=session['address'],
        Contact=session['contact'],
        Email=session['email'],
        Password=hex_dig
    )
    db.session.add(new_user)
    db.session.commit()
        
    # Clear session after saving user
    session.clear()

    return redirect(url_for('login'))  # Redirect to login after saving

    
    





if __name__ == "__main__":
    app.run(debug=True)
