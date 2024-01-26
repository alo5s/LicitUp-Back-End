import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()
def get_db_connection():
    try:
        db_connection = mysql.connector.connect(
            host=os.environ.get('MYSQLHOST'),
            user=os.environ.get('MYSQLUSER'),
            password=os.environ.get('MYSQLPASSWORD'),
            database=os.environ.get('MYSQLDATABASE'),
            port=os.environ.get('MYSQLPORT'),
        )
        return db_connection
    except mysql.connector.Error as err:
        print("Error de conexión a la base de datos:", err)
        return None
    except Exception as e:
        print("Error desconocido:", e)
        return None