from flask import Flask, render_template, request
import mysql.connector
import json
import os

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': '',  
    'database': 'adet'
}

def get_db_connection():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        form_data = {
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "contact_number": request.form.get('contact_number'),
            "email": request.form.get('email'),
            "address": request.form.get('address')
        }

        # Save data to the MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
                          VALUES (%s, %s, %s, %s, %s, %s)''', 
                          (form_data['first_name'], form_data['middle_name'], form_data['last_name'], 
                           form_data['contact_number'], form_data['email'], form_data['address']))

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('index.html', submitted=True)

    return render_template('index.html', submitted=False)

if __name__ == '__main__':
    app.run(debug=True)