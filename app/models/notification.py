# models/notification.py

from ..database.db import get_db_connection   # la conexión de la base de dato

class NotificationModel:
    @staticmethod
    def licitaciones():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                    SELECT l.CodigoExterno, l.CodigoEstado
                    FROM licitaciones l
                    """
                cursor.execute(sql)
                licitaciones = cursor.fetchall()
        
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return licitaciones
    

    @staticmethod
    def segumientos_comprobar_segumiento(codigo_licitacion):
        notificar_usario =[] 
        try:
            conn = get_db_connection()

            with conn.cursor() as cursor:
                # Obtener la ID de la Licitación si está en seguimiento
                sql_get_licitacion_id = "SELECT id FROM licitaciones WHERE CodigoExterno = %s"
                cursor.execute(sql_get_licitacion_id, (codigo_licitacion,))
                id_licitacion = cursor.fetchone()

                if id_licitacion:
                    # Obtener todos los usuarios que siguen esa Licitación
                    sql_get_usuario_id = "SELECT id_usuario FROM seguimiento WHERE id_licitacion = %s"
                    cursor.execute(sql_get_usuario_id, (id_licitacion,))
                    id_usuarios = cursor.fetchone()
                    
                    if id_usuarios:
                        notificar_usario.append(id_usuarios)
                    
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()

        return notificar_usario


    @staticmethod
    def segumientos_datos_usario(id_usarios):
        try:
            conn = get_db_connection()

            with conn.cursor() as cursor:
                if id_usarios:
                    # Obtener los datos de los usuarios que siguen la Licitación, como el correo y la ID
                    usuario_data = []
                    for usuario_id in id_usarios:
                        sql_get_usuario_datos = "SELECT id, correo FROM usuarios WHERE id = %s"
                        cursor.execute(sql_get_usuario_datos, (usuario_id,))
                        usuario_dato = cursor.fetchone()
                        usuario_data.append(usuario_dato)

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()

        return usuario_data