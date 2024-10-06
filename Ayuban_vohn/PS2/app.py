from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = {
        'first_name': request.form['first_name'],
        'middle_name': request.form['middle_name'],
        'last_name': request.form['last_name'],
        'contact_number': request.form['contact_number'],
        'email_address': request.form['email_address'],
        'address': request.form['address']
    }

    try:
        with open('registration_data.json', 'a') as f:
            f.write(jsonify(data))
            f.write('\n')  # Add a newline for readability
        return "Registration successful!"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)