from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import mysql.connector
import configparser
from mysql.connector import Error, errorcode

app = Flask(__name__)
bootstrap = Bootstrap(app)

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

@app.route('/')
def my_form():
    return render_template('user.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Get data from the form
    firstName = request.form.get('firstName')
    middleName = request.form.get('middleName')
    lastName = request.form.get('lastName')
    contact = request.form.get('contact')
    email = request.form.get('email')
    address = request.form.get('address')

    # Establish database connection
    connection = connect_to_db()
    if connection is None:
        return 'Database connection failed.'

    try:
        cursor = connection.cursor()

        # SQL query to insert data into the database
        sql_query = """INSERT INTO adet_user (firstName, middleName, lastName, contact, email, address)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_query, (firstName, middleName, lastName, contact, email, address))

        # Commit the changes
        connection.commit()

        return 'Form submitted successfully!'

    except Error as e:
        return f'Error occurred: {e}'

    finally:
        if connection.is_connected():
            cursor.close()
            
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
