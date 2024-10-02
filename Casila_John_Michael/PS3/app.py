from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    "host": "localhost",       # Change this to your MySQL server host
    "user": "root",            # Your MySQL username
    "password": "",    # Your MySQL password
    "database": "ps3"   # Your database name
}

def save_to_db(data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        sql = """
        INSERT INTO users (first_name, middle_name, last_name, contact_number, email, address)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (data["First Name: "], data["Middle Name: "], data["Last Name: "],
                  data["Contact Number: "], data["Email: "], data["Address: "])

        cursor.execute(sql, values)
        connection.commit()
        return "Your entry has been saved to the database!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        connection.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/save", methods=["POST"])
def save():
    data = {
        "First Name: ": request.form.get("fname"),
        "Middle Name: ": request.form.get("mname"),
        "Last Name: ": request.form.get("lname"),
        "Contact Number: ": request.form.get("contact"),
        "Email: ": request.form.get("email"),
        "Address: ": request.form.get("address")
    }

    # Call the function to save the data to the MySQL database
    return save_to_db(data)

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
