from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# Configure the instance path for Flask to store data files
app.config['INSTANCE_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')

@app.route('/')
def index():
    """Renders the registration form template."""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    """Processes registration data and saves it to JSON file."""
    data = {
        'firstname': request.form['firstname'],
        'middlename': request.form.get('middlename', ''),  # Handle optional middle name
        'lastname': request.form['lastname'],
        'contact_number': request.form['contact_number'],
        'email': request.form['email'],
        'address': request.form['address']
    }

    # Ensure the instance folder exists
    os.makedirs(app.config['INSTANCE_PATH'], exist_ok=True)

    file_path = os.path.join(app.config['INSTANCE_PATH'], 'registrations.json')

    # Load existing registrations or create a new list
    registrations = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                registrations = json.load(f)
            except json.JSONDecodeError:
                # In case the file is empty or invalid, start with an empty list
                registrations = []

    # Append new registration data
    registrations.append(data)

    # Write back to the JSON file
    with open(file_path, 'w') as f:
        json.dump(registrations, f, indent=4)

    return jsonify({'message': 'Registration successful!'})

if __name__ == '__main__':
    app.run(debug=True)
