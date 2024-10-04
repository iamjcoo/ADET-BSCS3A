from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',                  # Database host
    'user': 'root',                       # Your MySQL username
    'password': '',                        # Replace with your actual password
    'database': 'adets'                   # Your database name
}

def create_database_and_table():
    try:
        # Connect to MySQL server (without specifying a database)
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        cursor = connection.cursor()
        
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        cursor.execute(f"USE {db_config['database']}")
        
        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adets_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100),
                middle_name VARCHAR(100),
                last_name VARCHAR(100),
                contact_number VARCHAR(15),
                email VARCHAR(100),
                address TEXT
            )
        """)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()  # Close the connection after operations

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    form_data = {
        'first_name': request.form.get('first_name'),
        'middle_name': request.form.get('middle_name'),
        'last_name': request.form.get('last_name'),
        'contact_number': request.form.get('contact_number'),
        'email': request.form.get('email'),
        'address': request.form.get('address')
    }

    print(f"Received data: {form_data}")

    try:
        # Connect to the database directly in this route
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO adets_user (first_name, middle_name, last_name, contact_number, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(form_data.values()))
        
        connection.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()  # Close the connection after operations

    return redirect(url_for('register'))

if __name__ == "__main__":
    create_database_and_table()  # Create the database and table on startup
    app.run(debug=True)
