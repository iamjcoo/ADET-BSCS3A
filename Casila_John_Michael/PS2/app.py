from flask import Flask, render_template, request
import json #handles json files


app = Flask(__name__) #initialize

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/save", methods=["POST"])
def save():
    data = {
        "First Name: ": request.form.get("fname"),
        "Middle Name: ": request.form.get("mname"),
        "Last Name: ": request.form.get("lname"),
        "Contact Number: ": request.form.get("contact"),
        "Email: ": request.form.get("email"),
        "Address: ": request.form.get("address")
        
    }
    file_path = "out.json"
    
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent = 4)
            return f"Your entry has been save to \"{file_path}\""
    
    except FileExistsError:
        return "File already exists!"
    

@app.route("/<usr>") 
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
