from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    fname = None
    if request.method == 'POST':
        if 'sign_out' in request.form:
            return redirect(url_for('index'))
        fname = request.form.get('fname')
        mname = request.form.get('mname')
        lname = request.form.get('lname')
        num = request.form.get('num')
        email = request.form.get('email')
        address = request.form.get('address')

        user_data = {
            "first_name": fname,
            "middle_name": mname,
            "last_name": lname,
            "contact_number": num,
            "email_address": email,
            "address": address
        }
        #This checks whether the user.json is present, if yes appends the userData, if not creates then append
        try:
            try:
                with open('users.json', 'a') as json_file:
                    json_file.write(json.dumps(user_data) + '\n')
            except FileNotFoundError:
                with open('users.json', 'w') as json_file:
                    json.dump([user_data], json_file)
            return redirect(url_for('greet', fname=fname))

        except Exception as e:
            print("Error writing to file:", e)
            return render_template('index.html', fname=fname, error="Error saving data. Please try again.")
    else:
        return render_template('index.html', fname=fname)

@app.route('/greet')
def greet():
    fname = request.args.get('fname')
    return render_template('greet.html', fname=fname)

if __name__ == '__main__':
    app.run(debug=True)
