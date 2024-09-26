from flask import Flask, request, render_template

# Create a Flask application instance
app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return '''
        <h1>Hello World</h1>
        <form action="/greet" method="POST">
            <label for="name">Enter your name:</label>
            <input type="text" id="name" name="name" required>
            <input type="submit" value="Submit">
        </form>
    '''

# Route to handle form submission and process the entered name
@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']  # Retrieve the entered name from the form
    return f"Hello World! {name}, welcome to CCCS 106 - Applications Development and Emerging Technologies"

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
