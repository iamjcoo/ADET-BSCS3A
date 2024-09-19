from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def registration_form():
    return render_template('registration_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email_address = request.form.get('email_address')

    form_data = {
        'First Name': first_name,
        'Middle Name': middle_name,
        'Last Name': last_name,
        'Contact Number': contact_number,
        'Email Address': email_address
    }

    json_file = os.path.join('data', 'registration_data.json')
    with open(json_file, 'w') as f:
        json.dump(form_data, f, indent=4)

    return jsonify({"message": "Registration successful!", "data": form_data})

if __name__ == '__main__':
    app.run(debug=True)