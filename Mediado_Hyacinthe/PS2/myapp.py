from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data = {
        "first_name": request.form['first_name'],
        "middle_name": request.form['middle_name'],
        "last_name": request.form['last_name'],
        "contact_number": request.form['contact_number'],
        "email_address": request.form['email_address'],
        "address": request.form['address']
    }
    with open('registrations.json', 'a') as f:
        json.dump(data, f, indent=4)
        f.write('\n')
    flash('Registration successful')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)