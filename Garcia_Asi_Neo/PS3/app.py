from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)
config={'host':'localhost',
        'user':'root',
        'password':'',
        'database':'adet'}
def connect_db():
    conn = mysql.connector.connect(**config)
    return conn

@app.route('/')
def registration_form():
    return render_template('registration_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')

    form_data = {
        'First_Name': first_name,
        'Middle_Name': middle_name,
        'Last_Name': last_name,
        'Contact_Number': contact_number,
        'Email_Address': email_address
    }

    conn = connect_db()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (first_name, middle_name, last_name, contact_number, email_address))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Registration successful!", "data": form_data})

if __name__ == '__main__':
    app.run(debug=True)