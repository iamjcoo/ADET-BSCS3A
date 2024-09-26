from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# HTML template for the registration form using Bootstrap
@app.route('/')
def index():
    return render_template('register.html')

# Handle form submission
@app.route('/register', methods=['POST'])
def register():
    # Get form data
    form_data = {
        'firstname': request.form.get('firstname'),
        'middlename': request.form.get('middlename'),
        'lastname': request.form.get('lastname'),
        'contact': request.form.get('contact'),
        'email': request.form.get('email'),
        'address': request.form.get('address')
    }

    # Save form data to a JSON file
    with open('registrations.json', 'a') as f:
        json.dump(form_data, f)
        f.write('\n')  # Append a newline for each record

    return jsonify({'message': 'Registration successful!'}), 200

if __name__ == '__main__':
    app.run(debug=True)