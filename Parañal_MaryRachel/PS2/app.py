import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ensure the "data" directory exists
DATA_DIR = 'data'
RECORDS_FILE = os.path.join(DATA_DIR, 'records.json')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Serve the registration form
@app.route('/')
def index():
    return render_template('form.html')

# Handle form submission and save data to "records.json"
@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    first_name = request.form['firstName']
    middle_name = request.form.get('middleName', '')
    last_name = request.form['lastName']
    contact_number = request.form['contactNumber']
    email = request.form['email']
    address = request.form['address']

    # Create a dictionary of user data
    user_data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "contact_number": contact_number,
        "email": email,
        "address": address
    }

    # Check if records file exists, if not create an empty list
    if not os.path.exists(RECORDS_FILE):
        records = []
    else:
        # Load existing records
        with open(RECORDS_FILE, 'r') as f:
            records = json.load(f)

    # Append new user data to the list of records
    records.append(user_data)

    # Save the updated records back to the JSON file
    with open(RECORDS_FILE, 'w') as f:
        json.dump(records, f, indent=4)

    # Redirect to the success page
    return redirect(url_for('success'))

# Render the success page
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/close-instructions')
def close_instructions():
    return render_template('close_instructions.html')

if __name__ == '__main__':
    app.run(debug=True)
