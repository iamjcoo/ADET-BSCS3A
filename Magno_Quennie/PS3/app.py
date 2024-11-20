from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime

# Create the Flask app instance
app = Flask(__name__)

# Define MySQL database connection details
db_config = {
    'user': 'your_actual_mysql_username',      # Replace with your actual MySQL username
    'password': 'your_actual_mysql_password',  # Replace with your actual MySQL password
    'host': 'localhost',                       # Update if your MySQL host is different
    'database': 'adet',                        # Database name
    'raise_on_warnings': True
}


@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Convert form data to a dictionary
    info = request.form.to_dict()
    
    # Add timestamp to the info dictionary
    info['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # SQL query to insert the form data into the 'adet_user' table
    insert_query = """
    INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Create a tuple with the form data
    record = (
        info['name'],             # Match the HTML input name
        info.get('middle_name', ''),  # Use get to avoid KeyError if not provided
        info['last_name'],        # Match the HTML input name
        info['contact_number'],   # Match the HTML input name
        info['email_address'],    # Match the HTML input name
        info['address'],          # Match the HTML input name
        info['timestamp']
    )

    try:
        # Execute the insert query
        cursor.execute(insert_query, record)
        conn.commit()  # Commit the transaction

        return jsonify({'message': 'Information saved successfully to the database!'})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'message': 'Failed to save information to the database.'}), 500
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
