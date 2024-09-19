from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)
data_file = 'users.json'

# Load existing data
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return []

# Save data to JSON file
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['firstname']
    middlename = request.form['middlename']
    lastname = request.form['lastname']
    contact = request.form['contact']
    email = request.form['email']
    address = request.form['address']
    users = load_data()
    
    # Check for existing user
    if any(user['email'] == email for user in users):
        return jsonify({'message': 'Email already exists!'}), 400

    new_user = {'firstname': firstname,'middlename':middlename, 'lastname': lastname, 'contact': contact, 'email': email, 'address': address}
    users.append(new_user)
    save_data(users)
    
    return jsonify({'message': 'Registration successful!'}), 201

if __name__ == '__main__':
    app.run(debug=True)