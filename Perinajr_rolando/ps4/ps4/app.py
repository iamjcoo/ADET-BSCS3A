from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random key for security

# Mock database to store user information
users = {}

def encrypt_password(password):
    """Encrypt the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def reroute():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        
        # Store user details in the mock database
        users[email] = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact': contact,
            'email': email,
            'address': address,
            'password': encrypt_password(password)
        }
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == encrypt_password(password):
            session['user'] = users[email]
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Display the user dashboard."""
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    return render_template('dashboard.html', **user)

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
