from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display "Hello, World!" and a form for name input
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        return render_template('index.html', message=f"Hello World! {name}, welcome to CCCS 106 - Applications Development and Emerging Technologies")
    return render_template('index.html', message="Hello, World!")

if __name__ == '__main__':
    app.run(debug=True)
