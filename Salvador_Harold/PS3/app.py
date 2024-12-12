from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',  # Update with your database host if different
    'user': 'root',  # Replace with your MySQL username
    'password': '',  
    'database': 'adet'  # Database name
}

@app.route('/')
def index():
    """Renders the registration form template."""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    """Processes registration data and saves it to MySQL database."""
    data = {
        'first_name': request.form['firstname'],
        'middle_name': request.form.get('middlename', ''),  # Handle optional middle name
        'last_name': request.form['lastname'],
        'contact_number': request.form['contact_number'],
        'email_address': request.form['email'],
        'address': request.form['address']
    }

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert the registration data
        query = """
        INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['first_name'],
            data['middle_name'],
            data['last_name'],
            data['contact_number'],
            data['email_address'],
            data['address']
        ))

        # Commit the transaction
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Registration successful!'})
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error: {str(err)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
