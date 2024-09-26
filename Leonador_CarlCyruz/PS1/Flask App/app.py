from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = request.form.get('name')
    if name == '':
        name = None
    return render_template("index.html", name=name, title="Hello World!")

app.run(host='0.0.0.0', port=81, debug=True)