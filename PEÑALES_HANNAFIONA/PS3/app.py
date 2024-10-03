from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

class Config:
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'fiona'
    DB_NAME = 'adet'  

DB_CONFIG = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'database': Config.DB_NAME
}

def create_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def save_to_mysql(data):
    """Save user data to the MySQL database."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO adet_hanna (first_name, middle_name, last_name, contact_number, email_address, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data.get('first_name'),
                data.get('middle_name'),
                data.get('last_name'),
                data.get('contact_number'),
                data.get('email_address'),
                data.get('address')
            ))
            connection.commit()
            print("Data saved successfully to MySQL.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                connection.close()

def save_sql_to_file(data):
    """Save the SQL insert statement to a file."""
    sql_file = 'insert_data.sql'
    insert_query = f"""
    INSERT INTO adet_hanna (first_name, middle_name, last_name, contact_number, email_address, address)
    VALUES ('{data.get('first_name')}', '{data.get('middle_name')}', '{data.get('last_name')}', 
            '{data.get('contact_number')}', '{data.get('email_address')}', '{data.get('address')}');
    """
    with open(sql_file, 'a') as f:
        f.write(insert_query + '\n')
    print(f"SQL query saved to {sql_file}.")

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the registration form and handle form submissions."""
    success_message = None
    if request.method == 'POST':
        data = {
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "contact_number": request.form.get('contact_number'),
            "email_address": request.form.get('email_address'),
            "address": request.form.get('address')
        }
        print("Form data:", data)
        save_to_mysql(data)  # Save data to MySQL
        save_sql_to_file(data)  # Save SQL to file
        success_message = "Successfully Registered!"
        print("Success message set:", success_message)

    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
