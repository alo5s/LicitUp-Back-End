import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        db_connection = psycopg2.connect(
            host=os.environ.get('POSTSQLHOST'),
            user=os.environ.get('POSTSQLUSER'),
            password=os.environ.get('POSTSQLPASSWORD'),
            database=os.environ.get('POSTGRESQLDATABASE'),
            port=os.environ.get('POSTSQLPORT'),
        )
        return db_connection
    except psycopg2.Error as err:
        print("Error de conexión a la base de datos:", err)
        return None
    except Exception as e:
        print("Error desconocido:", e)
        return None