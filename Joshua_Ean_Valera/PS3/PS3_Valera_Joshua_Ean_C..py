from flask import Flask, render_template, request, redirect, flash
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def registration_form():
    if request.method == 'POST':
        first_name = request.form.get('validationDefault01')
        middle_name = request.form.get('validationDefault02')
        last_name = request.form.get('validationDefault03')
        email = request.form.get('inputEmail4')
        password = request.form.get('inputPassword4')
        address = request.form.get('inputAddress')
        contact_number = request.form.get('inputContact')

        try:
            # Log the received input to check the data
            print(f"Received form data: {first_name}, {middle_name}, {last_name}, {email}, {password}, {address}, {contact_number}")

            db.add_user(first_name, middle_name, last_name, email, password, address, contact_number)
            flash('User successfully registered', 'success')
        except Exception as e:
            # Log the error in the console and show a flash message in the front-end
            print(f"Error during user registration: {str(e)}")
            flash(f"Error during registration: {str(e)}", 'danger')
            return redirect('/')

        return redirect('/')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
