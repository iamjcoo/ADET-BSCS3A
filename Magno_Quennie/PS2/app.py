from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email_address = request.form['email_address']
    address = request.form['address']

    data = {
        "name": name,
        "middle_name": middle_name,
        "last_name": last_name,
        "contact_number": contact_number,
        "email_address": email_address,
        "address": address
    }

    with open('UserData.json', 'a') as f:
        json.dump(data, f)

    return render_template('form.html', message="information saved successfully!")
if __name__ == '__main__':
    app.run(debug=True)