from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

class MyDatabase:
    def __init__(self, host, user, password = None, database = None):
        self.host = (host if host != None else 'localhost')
        self.user = (user if user != None else 'root')
        self.connect_type = 1
        
        if password != None:
            self.password = password
            self.connect_type = 2
        
        if database != None:
            self.database = database
            self.connect_type = 3
        
        if (password != None) and (database != None):
            self.connect_type = 4
        
    
    def connect(self, connect_type = 0):
        self.connect_type = (connect_type if connect_type != 0 else self.connect_type)
        match self.connect_type:
            case 1:
                db = mysql.connector.connect(
                    host = self.host,
                    user = self.user
                )

            case 2:
                db = mysql.connector.connect(
                    host = self.host,
                    user = self.user,
                    password = self.password
                )

            case 3:
                db = mysql.connector.connect(
                    host = self.host,
                    user = self.user,
                    database = self.database
                )
            case 4:
                db = mysql.connector.connect(
                    host = self.host,
                    user = self.user,
                    password = self.password,
                    database = self.database
                )
            case _:
                db = mysql.connector.connect()
            
        db_cur = db.cursor(buffered=True)
        
        return db, db_cur

db = MyDatabase(
    host='localhost',
    user='root',
    database='site_users'
)

try:
    mydb, mycur = db.connect()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("WARNING: Database not found on localhost. Creating a new one...")

        mydb, mycur = db.connect(1)

        mycur.execute("CREATE DATABASE site_users")
        mycur.execute("USE site_users")
        mycur.execute(
            "CREATE TABLE `registered_users` ("
            " `id` INT(11) NOT NULL AUTO_INCREMENT,"
            " `fname` VARCHAR(255) NOT NULL,"
            " `mname` VARCHAR(255) NOT NULL,"
            " `lname` VARCHAR(255) NOT NULL,"
            " `contact_no` VARCHAR(20) NOT NULL,"
            " `email_add` VARCHAR(255) NOT NULL,"
            " `address` VARCHAR(255) NOT NULL,"
            "PRIMARY KEY(id)"
            ")"
        )

        mydb.disconnect()

        mydb, mycur = db.connect()

@app.route('/', methods=['GET', 'POST'])
def index(name=None, title="Hello, World!", userExists=None):
    return render_template("index.html", name=name, title=title, userExists=userExists)

@app.route('/register', methods=['POST'])
def add_user():
    fname = request.form.get('fname')
    mname = request.form.get('mname')
    lname = request.form.get('lname')
    cnum = request.form.get('cnumber')
    eadd = request.form.get('eaddress')
    add = request.form.get('address')

    # check if the user has previously registered before
    mycur.execute("SELECT * FROM registered_users")
    regUsers = mycur.fetchall()
    print(regUsers)
    if regUsers != None:
        if True in [
                all([
                    (fname == user[1]),
                    (mname == user[2]),
                    (lname == user[3]),
                    (cnum == user[4]),
                    (eadd == user[5]),
                    (add == user[6])
                ])
            for user in regUsers]:
            userExists = True

    
        else:
            userExists = False
    
    else:
        userExists = False

    if all([x != '' for x in [fname, mname, lname, cnum, eadd, add]]):
        name = f"{fname} {mname} {lname}"
        
        if not userExists:
            query = "INSERT INTO registered_users VALUES (NULL, %s, %s, %s, %s, %s, %s)"
            val = (fname, mname, lname, cnum, eadd, add)
            mycur.execute(query, val)
            mydb.commit()

    else:
        name = None
    
    return index(name=name, title=("Hello, %s" % fname if fname != None else "Hello World!"), userExists=userExists)

app.run(host='192.168.1.11', port=81, debug=True)