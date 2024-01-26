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


class AdminModel:
    @staticmethod
    def ls_usuario():
        try:
            conn = get_db_connection()  # Asegúrate de tener esta función definida
            with conn.cursor() as cursor:
                sql = "SELECT correo, suscripcion FROM usuarios"
                cursor.execute(sql)
                data = cursor.fetchall()  

                if data:
                    return data  # Devuelve la primera fila si hay resultados
                else:
                    return None  # O devuelve None si no hay resultados
        finally:
            conn.close()
    
    @staticmethod
    def update_suscripcion(correo, suscripcion):
        try:
            conn = get_db_connection()  # Asegúrate de tener esta función definida
            with conn.cursor() as cursor:
                # Utiliza parámetros en la consulta para evitar SQL injection
                sql = "UPDATE usuarios SET suscripcion = %s WHERE correo = %s"
                cursor.execute(sql, (suscripcion, correo))
                conn.commit()  # Guarda los cambios en la base de datos
                return cursor.rowcount
        finally:
            conn.close()


    # Lista de favorito id_favortos
    @staticmethod
    def usario_estado(correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT suscripcion FROM usuarios WHERE correo = %s"
                cursor.execute(sql, (correo,))
                licitacion_id = cursor.fetchone()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return licitacion_id