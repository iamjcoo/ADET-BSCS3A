from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import json
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def display_form():
    return render_template('user.html')

@app.route('/submit', methods=['POST'])
def process_form():
    # Get data from the form
    first_name = request.form.get('firstName')
    middle_name = request.form.get('middleName')
    last_name = request.form.get('lastName')
    contact_number = request.form.get('contact')
    email_address = request.form.get('email')
    home_address = request.form.get('address')

    # Create a dictionary with the form data
    user_info = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'contact_number': contact_number,
        'email_address': email_address,
        'home_address': home_address
    }

    # Define the path to the JSON file
    json_file_path = 'user_data.json'

    # Check if the file already exists
    if os.path.exists(json_file_path):
        # Read existing data
        with open(json_file_path, 'r') as file:
            users_data = json.load(file)
    else:
        users_data = []

    # Append new user info
    users_data.append(user_info)

    # Write updated data to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(users_data, file, indent=4)

    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
