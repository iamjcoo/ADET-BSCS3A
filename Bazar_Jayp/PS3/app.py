from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/greetings", methods=['POST', 'GET'])
def hello():
    if request.method == "POST":
        first_name = request.form.get('fname')
        middle_name = request.form.get('mname')
        last_name = request.form.get('lname')
        contact_num = request.form.get('contact')
        email = request.form.get('email')
        address = request.form.get('address')

        fullname = first_name + ' ' + middle_name + ' ' + last_name

        try:
            conn = connectSQL()
            cursor = conn.cursor()

            query = "INSERT INTO adet_user (FirstName, MiddleName, LastName, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (first_name, middle_name, last_name, contact_num, email, address)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()

            message = "Record inserted successfully."
            color = "#00ff00"
        except(Exception):
            message = "Error inserting in the database!"
            color = "#dd0000"

        return render_template('index.html', name=fullname, message=message, color=color)
    
    return render_template('index.html')

def connectSQL():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "adet"
    )

    return mydb

if __name__ == '__main__':
    app.run(debug=True)
