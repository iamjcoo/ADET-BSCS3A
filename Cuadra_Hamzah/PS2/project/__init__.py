from flask import Flask, render_template, request, url_for, jsonify
from flask_assets import Environment, Bundle
import json

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
        data = request.get_json()
        fName = data.get('FirstName')
        mName = data.get('MiddleName')
        lName = data.get('LastName')
        contactNum = data.get('ContactNum')
        email = data.get('Email')
        address = data.get('Address')
        
        # Load and Save to existing data
        try:
            with open('project/static/src/json/registrationData.json', 'w') as json_file:
                json.dump(data, json_file)
        except FileNotFoundError:
            raise FileNotFoundError

        return jsonify({"message": "User registered successfully!"})