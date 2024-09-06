from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greeting', methods=['POST'])
def greeting():
    name = request.form['name']
    return f"Hello, World! {name}, welcome to CCCS 106 - Applications Development and Emerging Technologies"

if __name__ == '__main__':
    app.run(debug=True)