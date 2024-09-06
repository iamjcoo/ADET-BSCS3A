from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods =["GET", "POST"])
def index():
    if request.method == "POST":
       name = request.form.get("InputName") 
       return f"Hello World! {name}, Welcome to CCCS 106 - Applications Development and Emerging Technologies"
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)