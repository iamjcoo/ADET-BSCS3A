import mysql.connector
from config import Config

def init_app(app):
    pass  # Placeholder for future initialization logic

def add_user(first_name, middle_name, last_name, email, password, address, contact_number):
    connection = None
    cursor = None  # Initialize cursor variable
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,  # Empty string for no password
            database=Config.MYSQL_DB
        )
        
        print(f"Inserting: {first_name}, {middle_name}, {last_name}, {email}, {password}, {address}, {contact_number}")
        
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO adet_user (first_name, middle_name, last_name, email, password, address, contact_number) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, middle_name, last_name, email, password, address, contact_number)
        )
        connection.commit()
        print("User successfully inserted.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if connection:
            connection.rollback()  # Rollback the transaction in case of an error
        raise  # Re-raise the exception so it can be handled elsewhere

    finally:
        # Close the cursor and connection properly
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def get_all_users():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,  # Empty string for no password
            database=Config.MYSQL_DB
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM adet_user")
        users = cursor.fetchall()
        
        return users
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
