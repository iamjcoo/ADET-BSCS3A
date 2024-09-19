from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from flask_bootstrap import Bootstrap

#database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet',
}

#check connection to database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    fname = None
    if request.method == 'POST':
        if 'sign_out' in request.form:
            return redirect(url_for('index'))
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        num = request.form.get('num')
        email = request.form.get('email')
        address = request.form.get('address')

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (FirstName, MiddleName, LastName, CellphoneNumber, Email, HomeAddress) VALUES (%s, %s, %s, %s, %s, %s)",
                           (fname, mname, lname, num, email, address))
            conn.commit()
            return redirect(url_for('greet', fname=fname))
        except mysql.connector.Error as e:
            print("Error executing query:", e)
            return "Error: Unable to add data to the database."
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template('index.html', fname=fname)

@app.route('/greet')
def greet():
    fname = request.args.get('fname')
    return render_template('greet.html', fname=fname)

if __name__ == '__main__':
    app.run(debug=True)
