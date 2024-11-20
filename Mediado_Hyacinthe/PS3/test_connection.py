import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='user'
    )
    if connection.is_connected():
        print("Successfully connected to the database")
except mysql.connector.Error as error:
    print(f"Error connecting to MySQL: {error}")
finally:
    if connection.is_connected():
        connection.close()
