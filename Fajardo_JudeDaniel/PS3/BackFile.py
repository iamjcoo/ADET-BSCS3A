from flask import Flask, render_template, request
import mysql.connector
import configparser 
from mysql.connector import Error, errorcode

app = Flask(__name__)

def read_db_config(filename='config.ini', section='mysql'):
    """Read database configuration from a config file."""
    parser = configparser.ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file.')
    return db

def connect_to_db():
    """Establish a connection to the database."""
    db_config = read_db_config()
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print('Connected to MySQL Database')
            return connection
    except mysql.connector.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Error: Access Denied. Please check your username and password.')
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print('Error: Database does not exist.')
        else:
            print(f'Error: {e}')
    return None

# Route for the form
@app.route('/')
def index():
    return render_template('FrontFile.html')

# Route to handle form submission
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    first_name = request.form['firstName']
    middle_name = request.form['middleName']
    last_name = request.form['lastName']
    contact_number = request.form['contactNumber']
    email = request.form['email']
    address = request.form['address']

    # Create a dictionary with form data
    user_data = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'contact_number': contact_number,
        'email': email,
        'address': address
    }

    connection = connect_to_db()
    if connection is None:
        return 'Database connection failed.'

    try:
        cursor = connection.cursor()

        # SQL query to insert data into the database
        sql_query = """INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_query, (first_name, middle_name, last_name, contact_number, email, address))

        # Commit the changes
        connection.commit()

        return 'Form submitted successfully!'

    except Error as e:
        return f'Error occurred: {e}'

    finally:
        if connection.is_connected():
            cursor.close()
            
            connection.close()

    # Return the thank you message
        return render_template('PageTwo.html')

if __name__ == '__main__':
    app.run(debug=True)
