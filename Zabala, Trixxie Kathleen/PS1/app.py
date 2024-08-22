from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    return ('Hello World!' + text + ', ' + "Welcome to CCCS 106 - Applications Development and Emerging Technologies")

app.run(host='0.0.0.0' , port=81)