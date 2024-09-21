from flask import Flask, request, redirect, url_for, render_template, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9568203147',
    'database': 'adet'
        }

def get_connection():
    return mysql.connector.connect(**db_config)
 
        
@app.route("/")
def home():
    return render_template("home.html")

@app.route('/submit', methods = ['POST'])
def submit():
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email = request.form.get('email')
    address = request.form.get('address')
    
    
    connection = get_connection()
    cursor = connection.cursor()
    
    append_query = '''
        INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    
    cursor.execute(append_query, (first_name, middle_name, last_name, '0'+ contact_number, email, address))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('accept'))

@app.route('/accept')
def accept():
    return render_template('accept.html')

if __name__ == "__main__":
    app.run(debug=True)