from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Function to save form data to a JSON file
def save_to_json(data):
    with open('registrations.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')

# Route for the registration form
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form['address']

        # Simple validation
        if not first_name or not last_name or not contact_number or not email_address or not address:
            flash("Please fill out all required fields!")
            return redirect(url_for('register'))

        # Prepare data to save in JSON format
        form_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address
        }

        # Save the data
        save_to_json(form_data)

        flash('Registration successful!')
        return redirect(url_for('register'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
