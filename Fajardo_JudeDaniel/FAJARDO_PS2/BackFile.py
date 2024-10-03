from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Route for the form
@app.route('/')
def index():
    return render_template('FrontFile.html')

# Route to handle form submission
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    first_name = request.form['firstName']
    middle_name = request.form['middleName']
    last_name = request.form['lastName']
    contact_number = request.form['contactNumber']
    email = request.form['email']
    address = request.form['address']

    # Create a dictionary with form data
    user_data = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'contact_number': contact_number,
        'email': email,
        'address': address
    }

    # Try to load existing data from the JSON file, reset if it's corrupted
    try:
        with open('DataFile.json', 'r') as json_file:
            users = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []  # If the file doesn't exist or is corrupted, reset the list

    # Append new user data to the list
    users.append(user_data)

    # Save the updated list back to the JSON file
    with open('DataFile.json', 'w') as json_file:
        json.dump(users, json_file, indent=4)  # Writing back to the JSON file

    # Return the thank you message
    return render_template('PageTwo.html')

if __name__ == '__main__':
    app.run(debug=True)
