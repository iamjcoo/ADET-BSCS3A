from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret_key'  # for flashing messages

# Database configuration dictionary
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
        }

# Function to get a connection to the MySQL database
def get_connection():
    return mysql.connector.connect(**db_config)

# Route for the homepage and form submission (both GET and POST methods)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('First_Name').strip()
        middle_name = request.form.get('Middle_Name').strip()
        last_name = request.form.get('Last_Name').strip()
        contact_number = request.form.get('Contact_Number').strip()
        address = request.form.get('Address').strip()
        email = request.form.get('Email').strip()

        # Basic validation to ensure that all required fields are filled
        if not first_name or not last_name or not contact_number or not email:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))

        # Insert data into the MySQL database
        try:
            connect = get_connection()
            cursor = connect.cursor()
            
            # SQL query to insert form data into the 'adet_user' table
            query = """
                INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, address, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, middle_name, last_name, contact_number, address, email)
            
            # Execute the query, commit changes, and close the cursor and connection after the transaction
            cursor.execute(query, values)
            connect.commit()
            cursor.close()
            connect.close()
            
            # Success message after successful insertion        
            message = ('Registration successful! Your details have been recorded.')

            flash(message, 'success')
            return redirect(url_for('success'))
        
        # Handle any database-related errors
        except mysql.connector.Error as error:
            flash(f'Error: {error}', 'error')
            return redirect(url_for('index'))

    return render_template('index.html')

# Route for the success page (after successful form submission)
@app.route('/success')
def success():
    return render_template('success.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
