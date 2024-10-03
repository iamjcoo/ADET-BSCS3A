from flask import Flask, session, request, redirect, url_for, render_template, flash
import mysql.connector, hashlib

app = Flask(__name__)
app.secret_key = 'ADET_S3cr3t_K3y!@#'

@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = encrypt(request.form.get('password'))

        try:
            conn = connectSQL()
            cursor = conn.cursor()

            query = "SELECT * FROm adet_user WHERE Email = %s AND Password = %s"
            values = (email, password)

            cursor.execute(query, values)
            
            user = cursor.fetchone()

            if user:
                session['user_email'] = email
                session['user_name'] = user[1]

                flash("Login successful!", "success")

                return redirect(url_for('dashboard'))
            else:
                flash("Wrong email or password. Please try again.", "danger")

            cursor.close()
            conn.close()

        except Exception as e:
            flash("Login failed. Please try again.", "danger")
            print(e)

    return render_template('index.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        first_name = request.form.get('fname')
        middle_name = request.form.get('mname')
        last_name = request.form.get('lname')
        contact_num = request.form.get('contact')
        email = request.form.get('email')
        password = encrypt(request.form.get('password'))
        address = request.form.get('address')

        try:
            conn = connectSQL()
            cursor = conn.cursor()

            query = "INSERT INTO adet_user (FirstName, MiddleName, LastName, ContactNumber, Email, Password, Address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (first_name, middle_name, last_name, contact_num, email, password, address)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            
            flash("Registration Complete!", "success")

            return redirect(url_for('login'))

        except Exception as e:
            flash("Registration failed. Please try again.", "danger")
            print(e)
    
    return render_template('signup.html')

@app.route("/dashboard")
def dashboard():
    if 'user_name' in session:
        name = session['user_name']
        return render_template('dashboard.html', name=name)
    else:
        flash("You must login first!", "danger")
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

def connectSQL():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "adet"
    )

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
