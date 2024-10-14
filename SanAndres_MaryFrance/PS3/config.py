import os

class Config:
    # Database configuration
    DB_HOST = 'localhost'
    DB_NAME = 'adet'
    DB_USER = 'root'
    DB_PASSWORD = ''

    @staticmethod
    def get_db_config():
        return {
            'host': Config.DB_HOST,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD
        }
