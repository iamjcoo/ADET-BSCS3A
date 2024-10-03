from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def get_db_connection():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return conn

# added a redirect for http://127.0.0.1:5000 to the login route
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # existing email validator
        email = request.form.get('email')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM adet_user WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM adet_user WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return render_template('register.html', error="Email already exists. Please use a different email.")

        # Get form data
        form_data = {
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "contact_number": request.form.get('contact_number'),
            "email": request.form.get('email'),
            "address": request.form.get('address'),
            "password": hashlib.sha256(request.form.get('password').encode()).hexdigest()  
        }

        # Save data to the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                          (form_data['first_name'], form_data['middle_name'], form_data['last_name'], 
                           form_data['contact_number'], form_data['email'], form_data['address'],
                           form_data['password']))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT first_name, middle_name, last_name, contact_number, email, address FROM adet_user WHERE id = %s', (user_id,))
    user_details = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return render_template('dashboard.html', user_details=user_details)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
