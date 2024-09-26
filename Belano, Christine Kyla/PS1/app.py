from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('mess', name=name))
    return render_template('index.html')

@app.route('/mess/<name>')
def mess(name):
    return render_template('mess.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
