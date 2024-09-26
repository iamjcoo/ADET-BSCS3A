from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route ('/', methods=['POST'])
def index():
    text = request.form['text']
    return ('Hello World!' + text + ', welcome to CCCS 106 - Applications Development and Emerging Technologies!')

app.run(host='0.0.0.0', port=81)