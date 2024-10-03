from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Collect form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email_address = request.form.get('email_address')
        address = request.form.get('address')

        # Error handling (basic validation)
        errors = {}
        if not first_name or not first_name[0].isupper():
            errors['first_name'] = 'First Name is required and must start with a capital letter.'
        if not middle_name or not middle_name[0].isupper():
            errors['middle_name'] = 'Middle Name must start with a capital letter.'
        if not last_name:
            errors['last_name'] = 'Last Name is required.'
        if not email_address:
            errors['email_address'] = 'Email Address is required.'
        elif '@' not in email_address:
            errors['email_address'] = 'Email address must contain @.'
        if not contact_number:
            errors['contact_number'] = 'Contact Number is required.'
        elif len(contact_number) != 11:
            errors['contact_number'] = 'Contact Number must be exactly 11 digits.'

        # Validate address using custom function
        address_error = validate_address(address)
        if address_error:
            errors['address'] = address_error

        # If there are errors, render the form again with errors
        if errors:
            return render_template('form.html', errors=errors, user_data=request.form)

        # Prepare user data to save
        user_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address  
        }

        # Save user data to a text file
        save_user_data_to_file(user_data)

        # Generate a greeting message
        greeting = f"Hello, {first_name} {middle_name} {last_name}! Welcome to CCCS 106."

        # Render the 'submitted.html' template with user data and greeting
        return render_template('submitted.html', user_data=user_data, greeting=greeting)

    return render_template('form.html', errors=None, user_data={})


# Function to validate the address field
def validate_address(address):
    if not address or not address[0].isupper():
        return "Address must start with a capital letter."
    return None

# Function to save user data to a text file inside the 'user_data' folder
def save_user_data_to_file(user_data):
    try:
        # Define the path for the 'user_data' folder
        folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data')

        # Check if the folder exists, if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Define the file path inside the 'user_data' folder
        file_path = os.path.join(folder_path, 'user_data.txt')

        # Open the file in append mode and write the user data
        with open(file_path, 'a') as f:
            f.write(f"First Name: {user_data['first_name']}, "
                    f"Middle Name: {user_data['middle_name']}, "
                    f"Last Name: {user_data['last_name']}, "
                    f"Contact Number: {user_data['contact_number']}, "
                    f"Email Address: {user_data['email_address']}, "
                    f"Address: {user_data['address']}\n")
    except Exception as e:
        print(f"File save error: {e}")
        raise


if __name__ == '__main__':
    app.run(debug=True)
