from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection details
db_config = {
    'user': 'root',   # Default XAMPP MySQL user
    'password': '',   # Default XAMPP MySQL password (leave blank if not set)
    'host': 'localhost',
    'database': 'adet'
}

# Function to establish connection to MySQL (without a database)
def connect_without_db():
    return mysql.connector.connect(
        user=db_config['user'], 
        password=db_config['password'], 
        host=db_config['host']
    )

# Function to establish connection to MySQL (with a database)
def connect_with_db():
    return mysql.connector.connect(**db_config)

# Automatically create database and table if they don't exist
def create_db_and_table():
    # Connect without specifying a database
    conn = connect_without_db()
    cursor = conn.cursor()

    # Create the `adet` database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS adet")
    
    # Switch to the `adet` database
    cursor.execute("USE adet")

    # Create the `adet_user` table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS adet_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        middle_name VARCHAR(255),
        last_name VARCHAR(255) NOT NULL,
        contact_number VARCHAR(20) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        address TEXT
    )''')

    conn.commit()
    cursor.close()
    conn.close()

# Call the function to create the database and table on app start
create_db_and_table()

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']

        # Insert data into MySQL database
        conn = connect_with_db()
        cursor = conn.cursor()

        sql = '''INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
                 VALUES (%s, %s, %s, %s, %s, %s)'''
        val = (first_name, middle_name, last_name, contact_number, email, address)

        try:
            cursor.execute(sql, val)
            conn.commit()
            print("Record inserted successfully into adet_user")
        except mysql.connector.Error as error:
            print(f"Failed to insert record: {error}")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('success'))

@app.route('/success')
def success():
    return "<h1>Registration Successful!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
