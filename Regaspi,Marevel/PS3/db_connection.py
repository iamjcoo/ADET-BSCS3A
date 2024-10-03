import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="new_password",
        database="adet"
    )
