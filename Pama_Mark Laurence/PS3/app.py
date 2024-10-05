from flask import Flask, render_template, request
import mysql.connector
from config import db_config  # Importing the database configuration

app = Flask(__name__, template_folder='template')

def get_connection():
    
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None  # Indicate connection failure

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Access form data using request.form dictionary
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email_address = request.form['email_address']
    address = request.form['address']

    # Connect to the database
    connection = get_connection()

    if connection:
        try:
            cursor = connection.cursor()

            # Insert data into the database
            sql = """
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, middle_name, last_name, contact_number, email_address, address)
            cursor.execute(sql, values)
            connection.commit()

            # Success message to be displayed on the template
            message = "Information saved successfully!"

            # Redirect to "submitted.html" after successful insertion
            return render_template('user.html', message="Information saved successfully!")

        except mysql.connector.Error as err:
            print("Error:", err)
            message = "Error: Could not save information."  # Error message
            return render_template('user.html', message=message)

        finally:
            if connection:
                connection.close()  # Close the database connection

    else:
        # Handle connection failure (e.g., display an error message)
        message = "Error: Could not connect to the database."
        return render_template('user.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
