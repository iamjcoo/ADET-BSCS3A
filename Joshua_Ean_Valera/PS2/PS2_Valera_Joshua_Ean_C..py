from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

# Path to the JSON file
json_file_path = os.path.join("data", "submissions.json")

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w') as f:
        json.dump([], f)

@app.route('/', methods=['GET', 'POST'])
def registration_form():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('validationDefault01')
        middle_name = request.form.get('validationDefault02')
        last_name = request.form.get('validationDefault02')
        email = request.form.get('inputEmail4')
        password = request.form.get('inputPassword4')
        address = request.form.get('inputAddress')
        contact_number = request.form.get('inputContact')
        
        # Create a dictionary with the form data
        submission_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'address': address,
            'contact_number': contact_number
        }
        
        # Load existing data and append new data
        with open(json_file_path, 'r+') as f:
            data = json.load(f)
            data.append(submission_data)
            f.seek(0)
            json.dump(data, f, indent=4)
        
        return redirect('/')
    
    return render_template('index.html')

@app.route('/submissions', methods=['GET'])
def view_submissions():
    with open(json_file_path, 'r') as f:
        submissions = json.load(f)
    return jsonify(submissions)

if __name__ == '__main__':
    app.run(debug=True)
