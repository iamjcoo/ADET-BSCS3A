from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    
    # Define the path to the JSON file
    json_file_path = 'data.json'
    
    # Check if the file exists
    if os.path.exists(json_file_path):
        # Read the existing data
        with open(json_file_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Append the new data
    existing_data.append(data)

    # Write the updated data back to the file
    with open(json_file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

    return jsonify({'message': 'Registration successful!'}), 200

if __name__ == '__main__':
    app.run(debug=True)