from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'adet'

mysql = MySQL(app)

@app.route('/')
def index():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM adet_user")
    users = cursor.fetchall()
    cursor.close()

    return render_template('user.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    first_name = request.form['first_name']
    middle_name = request.form.get('middle_name', '')
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email_address = request.form['email_address']
    address = request.form.get('address', '')

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email_address, address) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (first_name, middle_name, last_name, contact_number, email_address, address)
    )
    conn.commit()
    cursor.close()

    # Redirect back to the homepage to show the updated user list
    return redirect(url_for('index'))

@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['id']
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')
    address = request.form.get('address')

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE adet_user SET first_name=%s, middle_name=%s, last_name=%s, contact_number=%s, email_address=%s, address=%s WHERE id=%s",
        (first_name, middle_name, last_name, contact_number, email_address, address, user_id)
    )
    conn.commit()
    cursor.close()

    # Redirect back to the homepage to show the updated user list
    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['id']

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM adet_user WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()

    # Redirect back to the homepage to show the updated user list
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
