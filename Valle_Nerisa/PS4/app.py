#˜”*°•.˜”*°• CCCS 106 - APPLICATION DEVELOPMENT & EMERGING TECHNOLOGIES | PROBLEM SET #4 •°*”˜"
#                                  VALLE, NERISA S.  |  BSCS -3A

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'adet'

mysql = MySQL(app)

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adet_user WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            if user['password'] == hashed_password:
                session['loggedin'] = True
                session['id'] = user['id']
                session['first_name'] = user['first_name']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('No account found with this email. Please register first.', 'warning')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        password = hash_password(request.form['password'])

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check if the email is already registered
        cursor.execute('SELECT * FROM adet_user WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('Account already exists! Please login.', 'danger')
            return redirect(url_for('login'))
        else:
            try:
                # Insert user data into the database
                cursor.execute(
                    'INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                    (first_name, middle_name, last_name, contact_number, email, address, password)
                )
                mysql.connection.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except MySQLdb.Error as e:
                flash(f"An error occurred: {str(e)}", 'danger')
                mysql.connection.rollback()
            finally:
                cursor.close()

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT first_name, middle_name, last_name, contact_number, email, address FROM adet_user WHERE id = %s', (session['id'],))
        user_details = cursor.fetchone()
        cursor.close()

        if user_details:
            return render_template('dashboard.html', user_details=user_details)
        else:
            flash('User details not found.', 'warning')
            return redirect(url_for('login'))
    else:
        flash('Please login to access the Dashboard.', 'danger')
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form.get('address', '')
        password = hash_password(request.form['password'])  # Hashing the password

        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, middle_name, last_name, contact_number, email, address, password)
        )
        conn.commit()
        cursor.close()

        flash('Registration successful! You can log in now.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['id']
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email = request.form.get('email')
    address = request.form.get('address')

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE adet_user SET first_name=%s, middle_name=%s, last_name=%s, contact_number=%s, email=%s, address=%s WHERE id=%s",
        (first_name, middle_name, last_name, contact_number, email, address, user_id)
    )
    conn.commit()
    cursor.close()

    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['id']

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM adet_user WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('first_name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)