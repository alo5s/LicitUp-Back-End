# models/auth.py

from ..database.db import get_db_connection   # la conexión de la base de dato

class AuthModel:
    @staticmethod
    def usuario_existente(correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT id FROM usuarios WHERE correo = %s"
                cursor.execute(sql, (correo,))
                existing_user = cursor.fetchone()
                return existing_user is not None
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
    
    @staticmethod
    def registrar_usuario(user_entity):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO usuarios (correo, contraseña_hash) VALUES (%s, %s)"
                cursor.execute(sql, (user_entity[0], user_entity[1]))
                conn.commit()
                affected_rows = cursor.rowcount
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    

    @staticmethod
    def obtener_contraseña(identifier):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:

                sql = "SELECT contraseña_hash FROM usuarios WHERE correo = %s"
                cursor.execute(sql, (identifier,))
                result = cursor.fetchone()

                if result:
                    contraseña_hash = result[0]
                    return contraseña_hash

                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()


    # Add favorito
    @staticmethod
    def add_favorito(id_liciation, correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Obtener el ID del usuario
                sql_get_user_id = "SELECT id FROM usuarios WHERE correo = %s"
                cursor.execute(sql_get_user_id, (correo,))
                id_usuario = cursor.fetchone()

                estado_notificacion = False
                if id_usuario:
                    # Insertar el favorito
                    sql_insert_favorito = "INSERT INTO seguimiento (id_licitacion, id_usuario, suscripcion_notificaciones ) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert_favorito, (id_liciation, id_usuario[0], estado_notificacion))
                    conn.commit()
                    affected_rows = cursor.rowcount
                    return affected_rows
                else:
                    # El usuario no existe
                    return 0
        except Exception as ex:
            # Manejar la excepción apropiadamente
            raise Exception("Error al agregar favorito: " + str(ex))
        finally:
            conn.close()

    # eliminar favorito
    @staticmethod
    def delete_favorito(id_licitacion, correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Obtener el ID del usuario
                sql_get_user_id = "SELECT id FROM usuarios WHERE correo = %s"
                cursor.execute(sql_get_user_id, (correo,))
                id_usuario = cursor.fetchone()

                if id_usuario:
                    # Eliminar el favorito
                    sql_delete_favorito = "DELETE FROM seguimiento WHERE id_licitacion = %s AND id_usuario = %s"
                    cursor.execute(sql_delete_favorito, (id_licitacion, id_usuario[0]))
                    conn.commit()
                    affected_rows = cursor.rowcount
                    return affected_rows
                else:
                    # El usuario no existe
                    return 0
        except Exception as ex:
            # Manejar la excepción apropiadamente
            raise Exception("Error al eliminar favorito: " + str(ex))
        finally:
            conn.close()


    # Lista de favorito id_favortos
    @staticmethod
    def lista_id_favorito(correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                
                sql = "SELECT id FROM usuarios WHERE correo = %s "
                cursor.execute(sql, (correo,))
                id_usario = cursor.fetchone()

                sql = " SELECT id_licitacion FROM seguimiento WHERE id_usuario = %s "
                
                cursor.execute(sql, (id_usario[0],))
                licitacion_id = cursor.fetchall()

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return licitacion_id