# PACKAGES
from flask import Flask, render_template, request, url_for, jsonify
from flask_assets import Environment, Bundle
import mysql.connector



# Database
def connectDB():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        database='adet'
    )

    return db



app = Flask(__name__)
assets = Environment(app)

# Create Bundle for Flask-Assets to compile and prefix SCSS/SASS to CSS
css = Bundle('src/sass/main.sass',
             filters=['libsass'],
             output='dist/css/styles.css',
             depends='src/sass/*.sass')

assets.register("asset_css", css)
css.build()


# URL Routes:
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        fName = request.form.get('FirstName')
        mName = request.form.get('MiddleName')
        lName = request.form.get('LastName')
        contactNum = request.form.get('ContactNum')
        email = request.form.get('Email')
        address = request.form.get('Address')

        try:
            conn = connectDB()
            cursor = conn.cursor()

            query = "INSERT INTO adet_user (FirstName, MiddleName, LastName, ContactNumber, Email, Address) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (fName, mName, lName, contactNum, email, address)

            cursor.execute(query, values)
            conn.commit()

            message = "User registered successfully!"
            color = '#70fa70'
        except(Exception):
            message = "Error: Failed to Register User!"
            color = '#a81b1b'
        finally:
            cursor.close()
            conn.close()
        
        return render_template('registration.html', message=message, color=color)