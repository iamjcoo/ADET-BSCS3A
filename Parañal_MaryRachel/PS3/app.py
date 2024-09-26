from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuration settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Leave empty if no password
app.config['MYSQL_DB'] = 'adet'

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        print("Connection successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None

@app.route('/')
def index():
    return render_template('form.html')  # Display the registration form

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['firstName']
        middle_name = request.form['middleName']
        last_name = request.form['lastName']
        contact_number = request.form['contactNumber']
        email = request.form['email']
        address = request.form['address']

        try:
            conn = get_db_connection()
            if conn is None:
                return "Database connection failed.", 500
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (first_name, middle_name, last_name, contact_number, email, address))
            
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('success'))

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return f"Error saving data: {e}", 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "An unexpected error occurred. Please try again.", 500

@app.route('/success')
def success():
    return render_template('success.html')  # Display success message

if __name__ == '__main__':
    app.run(debug=True)
