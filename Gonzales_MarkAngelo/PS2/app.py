from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Load or create the users.json file
def load_users():
    if not os.path.exists("users.json"):
        return []
    with open("users.json", "r") as file:
        return json.load(file)

def save_user(user_data):
    users = load_users()
    users.append(user_data)
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        user_data = {
            "first_name": request.form['first_name'],
            "middle_name": request.form['middle_name'],
            "last_name": request.form['last_name'],
            "contact_number": request.form['contact_number'],
            "email": request.form['email'],
            "address": request.form['address']
        }
        
        # Save data to JSON file
        save_user(user_data)
        
        # Redirect to success page
        return redirect(url_for('success'))

@app.route('/success')
def success():
    users = load_users()
    return render_template('success.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)
