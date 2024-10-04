from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Function to save data to JSON file
def save_to_json(data):
    json_file_path = 'user_data.json'
    
    # Check if file exists, and if it does, load existing data
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Append new data to the existing data
    existing_data.append(data)

    # Save back to the file
    with open(json_file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

# Function to validate address
def validate_address(address):
    if not address:
        return 'Address is required.'
    if address and address[0].isupper() == False:
        return 'Address must begin with a capital letter.'
    return None

@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Collect form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email_address = request.form.get('email_address')
        address = request.form.get('address')  

        # Error handling
        errors = {}
        if not first_name:
            errors['first_name'] = 'First Name is required.'
        if not last_name:
            errors['last_name'] = 'Last Name is required.'
        if not email_address:
            errors['email_address'] = 'Email Address is required.'
        elif '@' not in email_address:
            errors['email_address'] = 'Email address must contain @.'
        if not contact_number:
            errors['contact_number'] = 'Contact Number is required.'
        elif len(contact_number) != 11:
            errors['contact_number'] = 'Contact Number must be exactly 11 digits.'
        
        # Validate address using custom function
        address_error = validate_address(address)
        if address_error:
            errors['address'] = address_error

        # If there are errors, render the form again with errors
        if errors:
            return render_template('form.html', errors=errors, user_data=request.form)

        # Prepare data to save
        user_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address  
        }

        # Save data to JSON file
        save_to_json(user_data)

        # Prepare greeting message
        greeting = f"Hello, {first_name} {middle_name} {last_name}! Welcome to CCCS 106 - Applications Development and Emerging Technologies."

        # Render success template with user data and greeting
        return render_template('submitted.html', user_data=user_data, greeting=greeting)

    return render_template('form.html', errors=None, user_data={})

if __name__ == '__main__':
    app.run(debug=True)
