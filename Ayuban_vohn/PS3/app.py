from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder=r'C:\Users\admin\OneDrive\Desktop\Ayuban_ADET\ADET-BSCS3A\Ayuban_vohn\PS3\template')



mydb = mysql.connector.connect(
    host="localhost",  # Replace with your host if needed
    user="root",       # Replace with your user if needed
    password="",     # Replace with your password if needed
    database="adet"    # Use the database you created
)

mycursor = mydb.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form['address']

        sql = "INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (first_name, middle_name, last_name, contact_number, email_address, address)
        mycursor.execute(sql, val)
        mydb.commit()

        return "Registration successful!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)