import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',       
    'password': '',       
    'database': 'adet'     
}

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connection to MySQL was successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
