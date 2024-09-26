from flask import Flask, render_template, request, jsonify
import mysql.connector as  mc
from mysql.connector import errorcode

app = Flask(__name__)
try:
    mydb = mc.connect(
        host = 'localhost', 
        user = 'root',
        database = 'users'
    )
    mycursor = mydb.cursor()
except mc.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        mydb = mc.connect(
            host = 'localhost',
            user = 'root'
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE users")
        mycursor.execute("USE users")
        mycursor.execute(
            "CREATE TABLE accounts ("
            "   first_name VARCHAR(255) not null,"
            "   middle_name VARCHAR(255) not null,"
            "   last_name VARCHAR(255) not null,"
            "   contact_number VARCHAR(11) not null,"
            "   email TEXT not null,"
            "   address TEXT not null"
            ")"
        )

# Route for rendering the registration form
@app.route('/')
def registration_form():
    return render_template('form.html')

# Route for handling form submission and saving to JSON
@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect the form data
    first_name = request.form.get('firstName')
    middle_name = request.form.get('middleName')
    last_name = request.form.get('lastName')
    contact_number = request.form.get('contactNumber')
    email = request.form.get('email')
    address = request.form.get('address')
    
    query ="INSERT INTO accounts VALUES (%s,%s,%s,%s,%s,%s)"
    val = (first_name,middle_name,last_name,contact_number,email,address)
    mycursor.execute(query,val)
    mydb.commit()

    return "Registered"

if __name__ == '__main__':
    app.run(debug=True)
