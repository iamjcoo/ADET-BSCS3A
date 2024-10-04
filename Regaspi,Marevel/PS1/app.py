from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    greeting = f"Hello, World! {name}, welcome to CCCS 106 - Applications Development and Emerging Technologies"
    return render_template('index.html', greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True)