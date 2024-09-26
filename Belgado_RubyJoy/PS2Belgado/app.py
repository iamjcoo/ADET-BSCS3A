from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def load_data():
    with open('data.json') as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        first_name = request.form['first-name']
        middle_initial = request.form['middle-initial']
        last_name = request.form['last-name']
        address = request.form['address']
        email_address = request.form['email-address']
        contact_number = request.form['contact-number']
        

        
        welcome_message = f"Hello {first_name}, Welcome to CCS 106 - Applications Development and Emerging Technologies!        !"
        return render_template('welcome.html', message=welcome_message)
    
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def users():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)