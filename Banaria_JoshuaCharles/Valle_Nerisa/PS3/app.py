#˜”*°•.˜”*°• CCCS 106 - APPLICATION DEVELOPMENT & EMERGING TECHNOLOGIES | PROBLEM SET #3 •°*”˜"
#                                  VALLE, NERISA S.  |  BSCS -3A

from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
from wtforms import Form, StringField, validators

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# This configure MySQL database connection.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'adet'

mysql = MySQL(app)

# Create class for the registration form
class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    middle_name = StringField('Middle Name', [validators.Length(max=50)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    contact_number = StringField('Contact Number', [validators.Length(min=7, max=15), validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=200), validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Retrieve form data
        first_name = form.first_name.data
        middle_name = form.middle_name.data
        last_name = form.last_name.data
        contact_number = form.contact_number.data
        email = form.email.data
        address = form.address.data
        
        # Create a cursor to execute SQL query
        cur = mysql.connection.cursor()
        
        # Insert data into MySQL table
        cur.execute("""
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, middle_name, last_name, contact_number, email, address))
        
        # Commit the transaction
        mysql.connection.commit()

        cur.close()
        
        flash('Registration successful!', 'result')
        return redirect('/result')
    
    return render_template('index.html', form=form)

@app.route('/result')
def success():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)