from flask import Flask, session, request, redirect, url_for, render_template, jsonify, make_response
import mysql.connector
import hashlib

app = Flask(__name__)

app.secret_key = 'skey'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9568203147',
    'database': 'adet'
        }

def get_connection():
    return mysql.connector.connect(**db_config)

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -- LOG IN -- #
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username')
        password = request.form.get('password')
        encrypted_password = encrypt_password(password)
        
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Checks if the user exist within the database
        login_query = '''
            SELECT * FROM adet_user WHERE (email = %s OR username = %s) 
            AND password =  %s
        '''
        
        
        cursor.execute(login_query, (email_or_username, email_or_username, encrypted_password))
        user = cursor.fetchone()
        
        cursor.close()    
        connection.close()
        
        if user:
            session['username'] = user['username']
            return redirect(url_for('home_page'))
        else:
            return render_template('login.html', error = "Invalid Username, Email, Or Password.")
    
    return render_template('login.html')
    
# -- SIGN-UP -- #        
@app.route("/signup")
def signup_page():
    return render_template('signup.html')

@app.route('/submit', methods = ['POST'])
def submit():
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    address = request.form.get('address')
    contact_number = request.form.get('contact_number')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    encrypted_password = encrypt_password(password)
    
    connection = get_connection()
    cursor = connection.cursor()
    
    append_query = '''
        INSERT INTO adet_user ( first_name, 
                                middle_name, 
                                last_name, 
                                address, 
                                contact_number, 
                                username,
                                email,
                                password)
                                
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    cursor.execute(append_query, (first_name, 
                                  middle_name, 
                                  last_name, 
                                  address, 
                                  '0'+ contact_number, 
                                  username, 
                                  email, 
                                  encrypted_password))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return redirect(url_for('accept'))

# -- Accept Page -- #
@app.route('/accept')
def accept():
    return render_template('accept.html')


# -- Home Page -- #
@app.route('/dashboard')
def home_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
        SELECT first_name, 
               middle_name,
               last_name,
               contact_number,
               address
        FROM adet_user
        WHERE username = %s;
    '''
    cursor.execute(query, (username,))
    
    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    response = make_response(render_template('dashboard.html', user=user_data))
    response.headers['Cache-Control'] = 'no-store'  # Prevent caching
    return response

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove the username from session
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)