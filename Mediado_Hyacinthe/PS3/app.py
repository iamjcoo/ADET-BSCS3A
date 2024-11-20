import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

def connect_to_mysql():
    """Connects to the MySQL database and returns the connection and cursor."""
    try:
        mydb = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return mydb, mydb.cursor()
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")  # Log the error
        return None, None

def log_user_data_to_sql_file(data):
    """Logs user data to an SQL file."""
    sql_file = 'saved_data.sql'
    sql_entry = f"INSERT INTO adet_hya (first_name, middle_name, last_name, contact_number, email_address, address) VALUES " \
                f"('{data['first_name']}', '{data['middle_name']}', '{data['last_name']}', '{data['contact_number']}', " \
                f"'{data['email_address']}', '{data['address']}');\n"
    
    with open(sql_file, 'a') as f:
        f.write(sql_entry)

@app.route('/')
def registration_form():
    """Renders the registration form HTML template."""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    """Handles the registration form submission and saves the data to the database."""
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')
    address = request.form.get('address')

    # Basic form validation
    if not first_name or not last_name or not email_address or not contact_number:
        flash("Please fill in all the required fields.", "error")
        return redirect(url_for('registration_form'))

    mydb, mycursor = connect_to_mysql()
    if mycursor:
        try:
            sql = """
                INSERT INTO adet_hya 
                (first_name, middle_name, last_name, contact_number, email_address, address) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            val = (first_name, middle_name, last_name, contact_number, email_address, address)
            mycursor.execute(sql, val)
            mydb.commit()

            # Log user data to the SQL file
            saved_data = {
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'contact_number': contact_number,
                'email_address': email_address,
                'address': address
            }
            log_user_data_to_sql_file(saved_data)

            flash("Registration successful!", "success")
            return redirect(url_for('registration_form'))  # Redirect to a success or home page
        except mysql.connector.Error as error:
            mydb.rollback()
            print(f"Failed to insert data into MySQL: {error}")
            flash("An error occurred while registering. Please try again.", "error")
            return redirect(url_for('registration_form'))  # Redirect back to the form
        finally:
            # Ensure database connection is closed
            mycursor.close()
            mydb.close()
    else:
        flash("Unable to connect to the database.", "error")
        return redirect(url_for('registration_form'))  # Redirect back to the form

if __name__ == '__main__':
    app.run(debug=True)
