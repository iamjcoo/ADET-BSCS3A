from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/greetings", methods=['POST', 'GET'])
def hello():
    if request.method == "POST":
        first_name = request.form.get('fname')
        middle_name = request.form.get('mname')
        last_name = request.form.get('lname')
        contact_num = request.form.get('contact')
        email = request.form.get('email')
        address = request.form.get('address')

        fullname = first_name + ' ' + middle_name + ' ' + last_name

        data = {
            'firstname': first_name, 
            'middlename': middle_name, 
            'lastname': last_name, 
            'contact': contact_num,
            'email': email,
            'address': address
            }

        with open('Bazar.json', 'w') as js:
            json.dump(data, js)

        return render_template('index.html', name=fullname)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
