from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "adet"

def get_db_connection():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    return conn

@app.route("/")
def index():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["emailAddress"]
        password = request.form["password"]
        phone_number = request.form["contactNumber"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""INSERT INTO users (firstName, lastName, emailAddress, password, contactNumber)
                            VALUES (%s, %s, %s, %s, %s)""", (firstName, lastName, email, hashed_password, phone_number))
            conn.commit()
            return redirect(url_for("login"))
        except mysql.connector.Error as e:
            # Handle MySQL errors gracefully
            return f"Error registering user: {e}"
        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["emailAddress"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[3], password):
                # Successful login, render dashboard
                return render_template("dashboard.html", user=user)
            else:
                # Invalid credentials, display error message
                return "Invalid email or password"
        except mysql.connector.Error as e:
            # Handle MySQL errors gracefully
            return f"Login error: {e}"
        finally:
            cursor.close()
            conn.close()

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)