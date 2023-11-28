# models/home.py

from ..database.db import get_db_connection   # la conexión de la base de dato

class HomeModel:
    @staticmethod
    def count():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM licitaciones"
                cursor.execute(sql)
                data = cursor.fetchone()[0]  # Obtener el valor de COUNT(*)
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return data
