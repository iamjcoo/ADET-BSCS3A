from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def save_to_json(data):
    # Load existing data from the file if it exists
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    
    existing_data.append(data)

    # Save updated data to the file
    with open(DATA_FILE, 'w') as file:
        json.dump(existing_data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    success_message = None
    if request.method == 'POST':
        data = {
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "contact_number": request.form.get('contact_number'),
            "email_address": request.form.get('email_address'),
            "address": request.form.get('address')
        }
        print("Form data:", data) 
        save_to_json(data)
        success_message = "Successfully Registered!"
        print("Success message set:", success_message)  
    
    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)

