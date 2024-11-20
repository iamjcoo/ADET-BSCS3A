from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='adet'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = create_connection()
        if conn is None:
            return jsonify({'message': 'Database connection failed.'}), 500
        cursor = conn.cursor()
        select_query = "SELECT id FROM adet_user WHERE username = %s AND password = %s"
        cursor.execute(select_query, (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard', user_id=user[0]))
        else:
            return jsonify({'message': 'Invalid credentials.'}), 401
    return render_template('dashboard.html')
@app.route('/submit', methods=['POST'])
def submit():
    info = request.form.to_dict()
    info['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = create_connection()
    if conn is None:
        return jsonify({'message': 'Database connection failed.'}), 500
    cursor = conn.cursor()

    # Check for missing middle name
    middle_name = info.get('middle_name', '')

    # Check for duplicate username
    select_query = "SELECT id FROM adet_user WHERE username = %s"
    cursor.execute(select_query, (info.get('username', ''),))  # Handle missing username
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'message': 'Username already exists.'}), 400

    # Update insert query to include username
    insert_query = """
        INSERT INTO adet_user (username, first_name, middle_name, last_name, contact_number, email_address, address, password, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Add username to the record tuple
    record = (
        info.get('username', ''), 
        info['name'],
        middle_name,
        info['last_name'],
        info['contact_number'],
        info['email_address'],
        info['address'],
        info['password'],
        info['timestamp']
    )

    try:
        cursor.execute(insert_query, record)
        conn.commit()
        return redirect(url_for('login'))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'message': 'Failed to save information to the database.'}), 500
    finally:
        cursor.close()
        conn.close()
@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    conn = create_connection()
    if conn is None:
        return "Database connection failed", 500
    cursor = conn.cursor()
    select_query = "SELECT * FROM adet_user WHERE id = %s"
    cursor.execute(select_query, (user_id,))
    user = cursor.fetchone()
    if user:
        user_data = {
            'first_name': user[1],
            'middle_name': user[2],
            'last_name': user[3],
            'contact_number': user[4],
            'email_address': user[5],
            'address': user[6],
            'timestamp': user[7]
        }
        return render_template('dashboard.html', user=user_data)  # Pass user_data as user
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
