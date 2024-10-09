# Packages
## Web Backend
from flask import Flask, render_template, redirect, request, session

## Database
import mysql.connector

## Security
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

def connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="adet"
    )
    return db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'UserID' not in session:
            return redirect('login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('_index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        password = hashlib.sha256(password.encode()).hexdigest()
        fName = request.form.get('FirstName')
        lName = request.form.get('LastName')
        contactNum = request.form.get('ContactNum')
        address = request.form.get('Address')

        try:
            db = connection()
            cursor = db.cursor()
            cursor.execute("INSERT INTO adet_user (Email, Password, FirstName, LastName, ContactNumber, Address) VALUES (%s, %s, %s, %s, %s, %s)", (email, password, fName, lName, contactNum, address))
            db.commit()

            message = "Registration Successful!"
            color = '##70fa70'

            return render_template('registration.html', message=message, color=color)
        except (Exception):
            message = "Error: Failed to Register User!"
            color = '#a81b1b'

            return render_template('registration.html', message=message, color=color)
        finally:
            cursor.close()
            db.close()

            return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')
        password = hashlib.sha256(password.encode()).hexdigest()

        db = connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM adet_user WHERE Email = %s AND Password = %s", (email, password))
        user = cursor.fetchone()

        cursor.close()
        db.close()
        if user is not None:
            session['UserID'] = user['UserID']
            session['Email'] = user['Email']

            return redirect('dashboard')
        elif user is None:
            message = "Invalid Email or Password!"

            return render_template('login.html', message=message), 401
    return render_template('login.html')
        
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['UserID']
    db = connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Email, FirstName, LastName, ContactNumber, Address FROM adet_user WHERE UserID = %s", (user_id,))
    user_details = cursor.fetchone()

    cursor.close()
    db.close()
    
    return render_template('dashboard.html', user_details=user_details) 
