from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve the name from the form
        name = request.form.get('name', '')
        # Check if the name is not empty
        if name:
            # Render the personalized greeting page
            return render_template('greeting.html', name=name)
    # Render the initial content page with the form
    return render_template('registration.html')

@app.route('/submit', methods=['POST'])
def submit():
    firstname=request.form.get("firstname")
    middlename=request.form.get("middlename")
    lastname=request.form.get("lastname")
    contactnum=request.form.get("cpnum")
    email=request.form.get("email")
    address=request.form.get("address")
    
    data={
        "firstname": firstname,
        "middlename": middlename,
        "lastname": lastname,
        "contactnum": contactnum,
        "email": email,
        "address": address
    }
    
    with open("ps2.json", "a") as file:
        json.dump(data,file)
    
    return "Registered!"

if __name__ == '__main__':
    app.run(debug=True)