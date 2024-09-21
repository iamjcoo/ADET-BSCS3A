from flask import Flask, request, redirect, url_for, render_template, jsonify
import json

app = Flask(__name__)

def open_json():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('data.json', 'w') as file:
            json.dump([], file)
        return []

def save_to_json(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
        
        
@app.route("/")
def home():
    return render_template("home.html")

@app.route('/submit', methods = ['POST'])
def submit():
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    contact_number = request.form.get('contact_number')
    email = request.form.get('email')
    address = request.form.get('address')
    
    form_data = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'contact_number': '0' + contact_number,
        'email': email,  
        'address': address  
    }
    
    data = open_json()
    data.append(form_data)
    save_to_json(data)
    
    return redirect(url_for('accept'))

@app.route('/accept')
def accept():
    return render_template('accept.html')

if __name__ == "__main__":
    app.run(debug=True)