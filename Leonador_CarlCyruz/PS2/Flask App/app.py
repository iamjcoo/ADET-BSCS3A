from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    fname = request.form.get('fname')
    mname = request.form.get('mname')
    lname = request.form.get('lname')
    cnum = request.form.get('cnumber')
    eadd = request.form.get('eaddress')
    add = request.form.get('address')
    if all([x != '' for x in [fname, mname, lname, cnum, eadd, add]]):
        name = f"{fname} {mname} {lname}"
        
        with open(f"{lname}.json", "w") as json_file:
            json.dump(
                {
                    "first_name": fname,
                    "middle_name": mname,
                    "last_name": lname,
                    "contact_number": cnum,
                    "email_address": eadd,
                    "address": add
                },
                json_file
            )
    else:
        name = None

    return render_template("index.html", name=name, title="Hello World!")

app.run(host='0.0.0.0', port=81, debug=True)