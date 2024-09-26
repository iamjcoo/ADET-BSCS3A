from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

directory = 'directory'
json_file = os.path.join(directory, 'registrations.json')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        form_data = {
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "contact_number": request.form.get('contact_number'),
            "email": request.form.get('email'),
            "address": request.form.get('address')
        }

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(json_file):
            with open(json_file, 'w') as f:
                json.dump([], f)

        with open(json_file, 'r') as f:
            data = json.load(f)

        data.append(form_data)

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

        return render_template('index.html', submitted=True)

    return render_template('index.html', submitted=False)

if __name__ == '__main__':
    app.run(debug=True)
