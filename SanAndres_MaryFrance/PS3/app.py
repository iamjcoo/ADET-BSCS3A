from flask import Flask, request, render_template, redirect, url_for, flash
from mysql.connector import Error
import mysql.connector
import re
from config import Config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = Config.get_db_config()

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def log_user_data_to_sql_file(data):
    sql_file = 'user_data.sql'
    sql_entry = f"INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address) VALUES " \
                f"('{data['first_name']}', '{data['middle_name']}', '{data['last_name']}', '{data['contact_number']}', " \
                f"'{data['email_address']}', '{data['address']}');\n"
    
    with open(sql_file, 'a') as f:
        f.write(sql_entry)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    # Retrieve form data
    first_name = request.form.get('firstname')
    middle_name = request.form.get('middlename')
    last_name = request.form.get('lastname')
    contact_number = request.form.get('contact')
    email_address = request.form.get('email')
    address = request.form.get('address')

    # Validation
    if not first_name or not last_name or not contact_number or not email_address:
        flash("Error: Firstname, Lastname, Contact, and Email are required.", 'error')
        return redirect(url_for('index'))
    
    if not is_valid_email(email_address):
        flash("Error: Invalid email format.", 'error')
        return redirect(url_for('index'))

    user_data = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'contact_number': contact_number,
        'email_address': email_address,
        'address': address
    }

    connection = None
    cursor = None
    try:
        print("Connecting to the database...")
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connection successful!")
            cursor = connection.cursor()

            # Insert data
            insert_query = """
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (first_name, middle_name, last_name, contact_number, email_address, address))
            connection.commit()

            log_user_data_to_sql_file(user_data)
            flash("Registration successful!", 'success')
            return redirect(url_for('index'))

    except Error as e:
        error_message = f"Error while inserting data: {e}"
        print(error_message)
        flash(error_message, 'error')
        return redirect(url_for('index'))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
