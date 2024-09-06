from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import json
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def my_form():
    return render_template('user.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Get data from the form
    firstName = request.form.get('firstName')
    middleName = request.form.get('middleName')
    lastName = request.form.get('lastName')
    contact = request.form.get('contact')
    email = request.form.get('email')
    address = request.form.get('address')


    # Create a dictionary with the form data
    user_data = {
        'firstName': firstName,
        'middleName' : middleName,
        'lastName' : lastName,
        'contact' : contact,
        'email': email,
        'address' : address
    }

    # Define the path to the JSON file
    json_file_path = 'user_data.json'

    # Check if the file already exists
    if os.path.exists(json_file_path):
        # Read existing data
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Append new user data
    data.append(user_data)

    # Write updated data to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
