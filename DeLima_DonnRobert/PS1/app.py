"""
Application Development and Emerging Technologies
Problem Set 1

Donn Robert De Lima | BSCS3A
"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def helloworld():
    return "Hello World! :^)"

if __name__ == "__main__":
    app.run()