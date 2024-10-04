#˜”*°•.˜”*°• CCCS 106 - APPLICATION DEVELOPMENT & EMERGING TECHNOLOGIES | PROBLEM SET #2 •°*”˜"
#                                  VALLE, NERISA S.  |  BSCS -3A

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)

# This sets a secret key for flashing messages.
app.secret_key = 'secret_key_flash_messages'

# Define the file path where user records will be stored in JSON format.
path = os.path.join('data', 'user_records.json')

# Retrieve all stored user records from the JSON file.
def record_user():
    if not os.path.exists(path):  
        return []
    with open(path, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []      # If the file doesn't exist or there's an issue reading it this return an empty list.

# This saves new user record to the existing list of records and write the updated list back to the JSON file.
def record_save(new_user):
    user_records = record_user()      # Fetch existing records
    user_records.append(new_user)
    with open(path, 'w') as file:
        json.dump(user_records, file, indent=4)

# Meanwhile, this handle the user registration form.
@app.route('/', methods=['GET', 'POST'])
def reg_form():
    if request.method == 'POST':
        # Collect and strip form input to remove unnecessary spaces.
        first_name = request.form.get('FIRSTNAME').strip()
        middle_name = request.form.get('MIDDLENAME').strip()
        last_name = request.form.get('LASTNAME').strip()
        phone_num = request.form.get('PHONE_NUMBER').strip()
        home = request.form.get('HOME_ADDRESS').strip()
        email = request.form.get('EMAIL_ADDRESS').strip()

        # Serves as basic validation to ensure required fields are filled.
        if not first_name or not last_name or not phone_num or not email:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('reg_form'))

        # Create a dictionary to hold the user data.
        user_data = {
            'FIRSTNAME': first_name,
            'MIDDLENAME': middle_name,
            'LASTNAME': last_name,
            'PHONE_NUMBER': phone_num,
            'HOME_ADDRESS': home,
            'EMAIL_ADDRESS': email
        }

        # Save the user data to the JSON file.
        record_save(user_data)

        # Flash a success message and redirect to the result page.
        success_message = ('Registration complete! We appreciate you providing the required information.')
        flash(success_message, 'result')

        return redirect(url_for('result'))

    # Render the registration form (GET request).
    return render_template('index.html')

# Displays the result page that confirms the user's registration was successful.
@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)      # Start the Flask development server in debug mode.