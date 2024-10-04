from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# MySQL connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Change this if your MySQL server is not local
        user='root',  # Enter your MySQL username
        password='',  # Enter your MySQL password
        database='adet3a'  # Name of your database
    )
    return connection

# Function to save form data to MySQL database
def save_to_database(data):
    connection = get_db_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO adet3a_users (first_name, middle_name, last_name, contact_number, email_address, address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['contact_number'],
        data['email_address'],
        data['address']
    ))

    connection.commit()
    cursor.close()
    connection.close()

# Route for the registration form
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form['address']

        # Simple validation
        if not first_name or not last_name or not contact_number or not email_address or not address:
            flash("Please fill out all required fields!")
            return redirect(url_for('register'))

        # Prepare data for saving
        form_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address
        }

        # Save the data to MySQL
        save_to_database(form_data)

        flash('Registration successful!')
        return redirect(url_for('register'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
