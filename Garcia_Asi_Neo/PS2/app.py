from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/")
def registration_form():
    return render_template('registration_form.html')

@app.route("/greetings", methods=['POST', 'GET'])
def hello():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_num = request.form.get('contact_number')
        email = request.form.get('email_address')

        fullname = first_name + ' ' + middle_name + ' ' + last_name

        data = {
            'firstname': first_name, 
            'middlename': middle_name, 
            'lastname': last_name, 
            'contact': contact_num,
            'email': email,
            }

        with open('Garcia.json', 'w') as js:
            json.dump(data, js)

        return render_template('registration_form.html', name=fullname)
    
    return render_template('registration_form.html')

if __name__ == '__main__':
    app.run(debug=True)