from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__, template_folder='C:\\Users\\yayay\\Desktop\\APP DEV\\PS2\\template')

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Access form data using request.form dictionary
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email_address = request.form['email_address']
    address = request.form['address']

    data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "contact_number": contact_number,
        "email_address": email_address,
        "address": address
    }

    with open('user.json', 'a') as f:
        json.dump(data, f)

    # Return the template with a success message
    return render_template('user.html', message="Information saved successfully!")

if __name__ == '__main__':
    app.run(debug=True)