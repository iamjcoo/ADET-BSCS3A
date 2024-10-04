from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime

app = Flask(__name__)

# MySQL database configuration
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="soyahh",
  database="adet"
)

mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    info = request.form.to_dict()
    # Add timestamp
    info['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    sql = "INSERT INTO adet_user (firstName, middleName, lastName, contactNumber, emailAddress, address, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (info['firstName'], info['middleName'], info['lastName'], info['contactNumber'], info['emailAddress'], info['address'], info['timestamp'])
    
    mycursor.execute(sql, val)
    mydb.commit()

    return jsonify({'message': 'Information saved successfully!'})

if __name__ == '__main__':
    app.run(debug=True)