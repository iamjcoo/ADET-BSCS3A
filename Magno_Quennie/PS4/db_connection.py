import mysql.connector
from mysql.connector import Error

# Define MySQL database connection details
db_config = {
    'user': 'your_actual_mysql_username',      # Replace with your MySQL username
    'password': 'your_actual_mysql_password',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'adet',                        # Your database name
    'raise_on_warnings': True
}

def create_connection():
    """Create a database connection and return the connection object."""
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"Error: {e}")
    return connection
