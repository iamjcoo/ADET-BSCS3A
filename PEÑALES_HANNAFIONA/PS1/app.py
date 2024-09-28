from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name', '')
        greeting = f"Hello, {name}, welcome to CCCS 106 - Applications Development and Emerging Technologies"
        return render_template('index.html', greeting=greeting)
    return render_template('index.html', greeting=None)

if __name__ == '__main__':
    app.run(debug=True)
