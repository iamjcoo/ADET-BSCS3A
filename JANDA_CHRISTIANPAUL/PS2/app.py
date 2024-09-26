from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the JSON file
json_file_path = os.path.join(os.getcwd(), 'server.json')

# Ensure the JSON file exists and has an empty list at the beginning
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump([], json_file)  # Start with an empty list

# Helper function to load existing data from server.json
def load_data():
    if not os.path.exists(json_file_path):
        return []  # Return empty list if file does not exist
    try:
        with open(json_file_path, 'r') as json_file:
            return json.load(json_file)
    except json.JSONDecodeError:
        return []  # Return empty list if JSON is invalid or empty

# Helper function to save data back to server.json
def save_data(data):
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Route for rendering the registration form
@app.route('/')
def registration_form():
    return render_template('form.html')

# Route for handling form submission and saving to JSON
@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect the form data
    data = {
        "first_name": request.form.get('firstName'),
        "middle_name": request.form.get('middleName'),
        "last_name": request.form.get('lastName'),
        "contact_number": request.form.get('contactNumber'),
        "email": request.form.get('email'),
        "address": request.form.get('address')
    }

    # Load existing data from server.json
    existing_data = load_data()

    # Append the new form submission to the list of existing data
    existing_data.append(data)

    # Write the updated data back to server.json
    save_data(existing_data)

    return jsonify({"message": "Form submitted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
