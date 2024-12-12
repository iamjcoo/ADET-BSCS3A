from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_data = {
        "first_name": request.form.get('first_name'),
        "middle_name": request.form.get('middle_name'),
        "last_name": request.form.get('last_name'),
        "contact_number": request.form.get('contact_number'),
        "email": request.form.get('email'),
        "address": request.form.get('address')
    }

    with open('data/users.json', 'a') as json_file:
        json.dump(user_data, json_file)
        json_file.write('\n')

    return "Registration Successful!"

if __name__ == "__main__":
    app.run(debug=True)
