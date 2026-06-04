import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flask_login'
}

def get_conn():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print('\nDatabase berhasil terhubung')
            return conn
        else:
            print('\nDatabase gagal terhubung')
            return None
    except Error as e:
        print(f"Database Error: {e}")
        
if __name__ == "__main__":
    get_conn()