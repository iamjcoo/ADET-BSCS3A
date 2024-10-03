from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret_key'  # for flashing messages

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
        }

def get_connection():
    return mysql.connector.connect(**config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('First_Name').strip()
        middle_name = request.form.get('Middle_Name').strip()
        last_name = request.form.get('Last_Name').strip()
        contact_number = request.form.get('Contact_Number').strip()
        address = request.form.get('Address').strip()
        email = request.form.get('Email').strip()

        # Basic validation
        if not first_name or not last_name or not contact_number or not email:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))

         # Insert data into database
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, address, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, middle_name, last_name, contact_number, address, email)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
        
            message = ( "The registration form is now complete!" 
"Thank you for giving us the appropriate details." )

            flash(message, 'success')
            return redirect(url_for('success'))
        
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
            return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
