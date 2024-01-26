# models/home.py

from ..database.db import get_db_connection   # la conexión de la base de dato

class MapaModel:
    @staticmethod
    def mapa():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                SELECT u.id, u.ComunaUnidad, COUNT(l.id) AS Cantidad, u.latitud, u.longitud
                FROM ubicaciones u
                LEFT JOIN licitaciones l ON u.id = l.id_ComunaUnidad
                GROUP BY u.id, u.ComunaUnidad, u.latitud, u.longitud
                """
                cursor.execute(sql)
                data = cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return data


    @staticmethod
    def obtener_licitaciones_por_ubicacion(id_ubicacion, pagina=1, elementos_por_pagina=25):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Consulta SQL para obtener licitaciones por ID de ubicación con paginación
                offset = (pagina - 1) * elementos_por_pagina
                sql = """
                SELECT l.id, l.CodigoExterno, l.CodigoEstado, l.Descriptive_name, l.FechaCreacion
                FROM licitaciones AS l
                JOIN ubicaciones AS u ON l.id_ComunaUnidad = u.id
                WHERE u.id = %s
                LIMIT %s OFFSET %s
                """
                cursor.execute(sql, (id_ubicacion, elementos_por_pagina, offset))
                licitaciones = cursor.fetchall()
    
                # Consulta SQL para obtener el número total de registros sin paginación
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM licitaciones AS l
                    JOIN ubicaciones AS u ON l.id_ComunaUnidad = u.id
                    WHERE u.id = %s
                """, (id_ubicacion,))
                total_registros = cursor.fetchone()[0]
    
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
    
        return licitaciones, total_registros

    # Mapa de Usuario con sus preferencias:
    def mapa_usuario(ls_mapas):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                SELECT 
                    u.id, u.ComunaUnidad, u.latitud, u.longitud
                FROM 
                    ubicaciones u
                LEFT JOIN 
                    licitaciones l ON u.id = l.id_ComunaUnidad
                WHERE 
                    u.ComunaUnidad = ANY(%s)
                GROUP BY
                    u.id, u.ComunaUnidad, u.latitud, u.longitud
                """
                cursor.execute(sql, (ls_mapas,))
                data = cursor.fetchall()
        
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return data

    @staticmethod
    def licitaciones_perfil_mapa(parametro_perfil=None, pagina=1, comuna=None):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                nLicitaciones = int(list(parametro_perfil['nLicitacion'])[0])
                # Convertir conjuntos (sets) a listas
                salario_max = float(list(parametro_perfil['Salario_max'])[0])
                salario_min = float(list(parametro_perfil['Salario_min'])[0])

                # Código de estado
                estado = "5"

                productos = list(parametro_perfil.get('productos', []))
                codificaciones = list(parametro_perfil.get("codificaciones", []))

                # Convertir todos los elementos de la lista en minúsculas
                productos_lower = [p.lower() for p in productos]

                # Construir la consulta SQL base
                sql = """
                    SELECT 
                        l.id, l.CodigoExterno, l.CodigoEstado, l.Descriptive_name, l.FechaCreacion
                    FROM 
                        licitaciones AS l
                    JOIN 
                        ubicaciones AS u ON l.id_ComunaUnidad = u.id
                    WHERE 
                        LOWER(u.ComunaUnidad) = LOWER(%s)
                        
                """
                
                if codificaciones:
                    sql += " AND l.tipo_codificación = ANY(%s)"
                
                if estado:
                    sql += "AND l.codigoestado = ANY(%s)" 
                
                if salario_min is not None and salario_max is not None:
                    sql += " AND l.precio BETWEEN %s AND %s"
                
                if productos_lower:
                    # Utilizar operador % para coincidencias parciales
                    sql += " AND (LOWER(l.producto) LIKE ANY(%s) OR LOWER(l.Descriptive_name) LIKE ANY(%s))"
                    # Convertir productos_lower a minúsculas y agregar '%' alrededor de cada elemento
                    productos_lower_like = ['%' + p + '%' for p in productos_lower]
                    params = (comuna, codificaciones, [estado], salario_min, salario_max, productos_lower_like, productos_lower_like)

                else:
                    sql += " AND LOWER(l.Descriptive_name) LIKE ANY(%s)"
                    params = (comuna, codificaciones, [estado], salario_min, salario_max, productos_lower)

                elementos_por_pagina = 25
                # Calcula el offset y limit para la paginación
                offset = (pagina - 1) * elementos_por_pagina
                limite = elementos_por_pagina

                # Aplica paginación solo si hay más elementos que los especificados en la página
                if nLicitaciones < elementos_por_pagina:
                    sql += " LIMIT %s"
                    params += (nLicitaciones,)
                elif nLicitaciones > elementos_por_pagina:
                    sql += " OFFSET %s LIMIT %s"
                    params += (offset, limite)
                
                # Obtén los resultados de la consulta
                cursor.execute(sql, params)
                licitaciones = cursor.fetchall()


        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return licitaciones