from flask import Flask, render_template, request, jsonify
import json
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    info = request.form.to_dict()
    # Add timestamp
    info['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    data = {
    "firstName": info['firstName'], 
    "middleName": info['middleName'], 
    "lastName": info['lastName'], 
    "contactNumber": info['contactNumber'], 
    "emailAddress":info['emailAddress'], 
    "address": info['address'], 
    "timestamp": info['timestamp']
}

    # Save data to JSON file
    with open('user_info.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')  # Add a newline for better readability

    return jsonify({'message': 'Information saved successfully!'})

if __name__ == '__main__':
    app.run(debug=True)