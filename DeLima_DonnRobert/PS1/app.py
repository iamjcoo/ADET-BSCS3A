"""
Application Development and Emerging Technologies
Problem Set 1

Donn Robert De Lima | BSCS3A
"""

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def helloworld():
    return render_template('main.html')

@app.route('/', methods = ['GET','POST'])
def greeting():
    if request.method == 'POST':
        text = request.form.get('Name')
        if text == "":
            return render_template('main.html', text = 'Guest')
    return render_template('main.html', text = text)

    
if __name__ == "__main__":
    app.run()