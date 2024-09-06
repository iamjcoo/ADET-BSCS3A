from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/greetings", methods=['POST', 'GET'])
def hello():
    if request.method == "POST":
        name = request.form.get('name')

        return render_template('index.html', name=name)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
