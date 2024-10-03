from flask import Flask, render_template, request, redirect, session, flash
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key') 

users = {}

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email_address = request.form['email_address'] 
        password = encrypt_password(request.form['password'])
        users[username] = {'password': password, 'first_name': first_name, 'last_name': last_name, 'email_address': email_address}
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = encrypt_password(request.form['password'])
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Incorrect username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    user = users[session['username']]
    return render_template('dashboard.html', email_address=user['email_address'], first_name=user['first_name'], last_name=user['last_name'], username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
