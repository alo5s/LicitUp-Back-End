# models/segumientos.py

from ..database.db import get_db_connection   # la conexión de la base de dato

class SegumientosModel:
    @staticmethod
    def licitaciones_segumientos(correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Obtener el ID del usuario
                sql_get_user_id = "SELECT id FROM usuarios WHERE correo = %s"
                cursor.execute(sql_get_user_id, (correo,))
                id_usuario = cursor.fetchone()
                
                if id_usuario:
                    licitacion_sql = """
                        SELECT l.id, l.CodigoExterno, l.CodigoEstado, l.Descriptive_name, l.Nombre_del_Organismo, 
                               l.Producto, l.Precio, l.Cantidad, l.FechaCreacion, l.FechaPublicacion, 
                               l.FechaCerrada, l.FechaDesierta, l.FechaRevocada, l.FechaSuspendido, 
                               l.FechaAdjudicacion, u.ComunaUnidad, l.FechaInicio, l.FechaFinal, l.FechaPubRespuestas,
                               o.id AS id_orden_compra, o.CodigoExterno AS CodigoExterno_Orden, 
                               o.CodigoEstado AS CodigoEstado_Orden, o.Descriptive_name AS Descriptive_name_Orden,
                               o.Nombre_del_Organismo AS Nombre_del_Organismo_Orden,
                               o.FechaCreacion, o.FechaEnvio, o.FechaAceptacion, o.FechaCancelacion, o.FechaUltimaModificacion
                        FROM licitaciones l
                        INNER JOIN ubicaciones u ON l.id_ComunaUnidad = u.id
                        LEFT JOIN orden_de_compra o ON l.id = o.id_Licitacion
                        INNER JOIN seguimiento s ON l.id = s.id_licitacion
                        WHERE s.id_usuario = %s;
                        """
                    cursor.execute(licitacion_sql, (id_usuario[0],))

                    licitaciones = cursor.fetchall()
                else:
                    # El usuario no existe
                    return None
        
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return licitaciones

    
    # eliminar favorito
    @staticmethod
    def licitaciones_segumientos_delete(codigo_licitacion, correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Obtener el ID del usuario
                sql_get_user_id = "SELECT id FROM usuarios WHERE correo = %s"
                cursor.execute(sql_get_user_id, (correo,))
                id_usuario = cursor.fetchone()

                sql_get_licitacion_id = "SELECT id FROM licitaciones WHERE CodigoExterno = %s"
                cursor.execute(sql_get_licitacion_id, (codigo_licitacion,))
                id_licitacion = cursor.fetchone()
                
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