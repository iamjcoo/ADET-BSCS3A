from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # for flashing messages

INFO = os.path.join('data', 'record.json')

def load_users():
    if not os.path.exists(INFO):
        return []
    with open(INFO, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_user(user):
    users = load_users()
    users.append(user)
    with open(INFO, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('First_Name').strip()
        middle_name = request.form.get('Middle_Name').strip()
        last_name = request.form.get('Last_Name').strip()
        contact_number = request.form.get('Contact_Number').strip()
        address = request.form.get('Address').strip()
        email = request.form.get('Email').strip()

        # Basic validation
        if not first_name or not last_name or not contact_number or not email:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))

        # Create user dictionary
        user = {
            'First_Name': first_name,
            'Middle_Name': middle_name,
            'Last_Name': last_name,
            'Contact_Number': contact_number,
            'Address': address,
            'Email': email
        }

        # Save user to JSON file
        save_user(user)
        
        message = ('You have completed the registration form! '
            'Thank you for providing the required information.')

        flash(message, 'success')
        return redirect(url_for('success'))

    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
