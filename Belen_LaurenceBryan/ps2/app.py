from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def registration_form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Process the form data
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')
    address = request.form.get('address')

    # Create a dictionary with the form data
    form_data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "contact_number": contact_number,
        "email_address": email_address,
        "address": address
    }

    # Save the data to a JSON file
    save_to_json(form_data)

    # Redirect to a thank you page or back to the form
    return redirect(url_for('registration_form'))

def save_to_json(data):
    # Define the path for the JSON file
    json_file_path = 'registrations.json'

    # Check if the file exists
    if os.path.exists(json_file_path):
        # If it exists, read the current data
        with open(json_file_path, 'r') as file:
            current_data = json.load(file)
    else:
        # If it doesn't exist, start with an empty list
        current_data = []

    # Append the new registration data
    current_data.append(data)

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(current_data, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
