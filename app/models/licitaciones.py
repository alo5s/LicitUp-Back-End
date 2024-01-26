# models/home.py

from ..database.db import get_db_connection   # la conexión de la base de dato

class LicitacionesModel:
    @staticmethod
    def ts_2(pagina=1, elementos_por_pagina=25, estado=None, fecha_inicial=None, fecha_final=None, orden=None):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                fecha_column = None

                if estado == 5:
                    fecha_column = "FechaPublicacion"
                elif estado == 6:
                    fecha_column = "FechaCerrada"
                elif estado == 7:
                    fecha_column = "FechaDesierta"
                elif estado == 8:
                    fecha_column = "FechaAdjudicacion"
                elif estado ==  18:
                    fecha_column = "FechaRevocada"
                elif estado == 19:
                    fecha_column = "FechaSuspendido"

                
                else:
                    fecha_column = "FechaCreacion"

                params = []

                sql = f"SELECT id, CodigoExterno, CodigoEstado, Descriptive_name, {fecha_column} FROM licitaciones WHERE 1=1"

                if fecha_inicial and fecha_final:
                    sql += f" AND DATE({fecha_column}) >= %s AND DATE({fecha_column}) <= %s"
                    params.extend([fecha_inicial, fecha_final])
        

                elif fecha_final:
                    sql += f" AND DATE({fecha_column}) = %s"
                    params.append(fecha_final)


                if estado:
                    sql += f" AND CodigoEstado = %s::character varying"  # Conversión explícita
                    #sql += f" AND CodigoEstado = %s"
                    params.append(estado)

                if orden == "asc":
                    sql += f" ORDER BY {fecha_column} ASC"
                elif orden == "desc":
                    sql += f" ORDER BY {fecha_column} DESC"

                cursor.execute(sql, params)
                datos = cursor.fetchall()

                # Obtén el número total de registros en la tabla
                total_registros = len(datos)
                # Calcula el offset y limit para la paginación
                offset = (pagina - 1) * elementos_por_pagina
                limite = elementos_por_pagina

                # Aplica paginación solo si hay más elementos que los especificados en la página
                if total_registros > offset:
                    sql += " LIMIT %s OFFSET %s"
                    params.extend([limite, offset])  # Extiende la lista de parámetros
                    cursor.execute(sql, params)
                    datos = cursor.fetchall()
                else:
                    datos = []
        
                #print(sql)
        
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos, total_registros
    
    @staticmethod
    def srec(descriptive_name, codigo_externo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                if descriptive_name:
                    sql = "SELECT id, CodigoExterno, CodigoEstado, Descriptive_name, FechaCreacion FROM licitaciones WHERE Descriptive_name LIKE %s"
                    cursor.execute(sql, ('%' + descriptive_name + '%',))
                elif codigo_externo:
                    sql = "SELECT id, CodigoExterno, CodigoEstado, Descriptive_name, FechaCreacion FROM licitaciones WHERE CodigoExterno LIKE %s"
                    cursor.execute(sql, ('%' + codigo_externo + '%',))
                else:
                    return []  # Si no se proporciona un criterio de búsqueda válido, devuelve una lista vacía.

                data = cursor.fetchall()  # Obtener todas las filas que coincidan con la consulta

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return data
    
    @staticmethod
    def detalle(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Consulta para obtener la información de la licitación
                sql = """
                    SELECT l.CodigoExterno, l.CodigoEstado ,l.Descriptive_name, l.Nombre_del_Organismo, l.Producto,
                           l.Precio, l.Cantidad, l.FechaCreacion, l.FechaPublicacion, l.FechaCerrada,
                           l.FechaDesierta, l.FechaRevocada, l.FechaSuspendido, l.FechaAdjudicacion, u.ComunaUnidad
                    FROM licitaciones l
                    INNER JOIN ubicaciones u ON l.id_ComunaUnidad = u.id
                    WHERE l.id = %s
                """
                cursor.execute(sql, (id,))
                licitacion = cursor.fetchone()
                
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return licitacion
    
    @staticmethod
    def licitaciones_perfil(parametro_perfil=None, pagina=1):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                nLicitaciones = int(list(parametro_perfil['nLicitacion'])[0])
                #parametro_perfil['nLicitacion']
                # Convertir conjuntos (sets) a listas
                salario_max = float(list(parametro_perfil['Salario_max'])[0])
                salario_min = float(list(parametro_perfil['Salario_min'])[0])

                # Codiog de estado
                estado = "5"
                # Convertir conjuntos (sets) a listas
                ciudades = list(parametro_perfil.get('ciudades', []))
                productos = list(parametro_perfil.get('productos', []))
                codificaciones = list(parametro_perfil.get("codificaciones", []))
                # Convertir toda los elemento de la lista en low:
                productos_lower = [p.lower() for p in productos]

                # Construir la consulta SQL base  WHERE u.ComunaUnidad IN %s
                sql = """
                    SELECT l.id, l.CodigoExterno, l.CodigoEstado, l.Descriptive_name, l.FechaCreacion
                    FROM licitaciones AS l
                    JOIN ubicaciones AS u ON l.id_ComunaUnidad = u.id
                    WHERE u.ComunaUnidad = ANY(%s)
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
                    params = (ciudades, codificaciones, [estado], salario_min, salario_max, productos_lower_like, productos_lower_like)
                else:
                    sql += " AND LOWER(l.Descriptive_name) LIKE ANY(%s)"
                    params = (ciudades, codificaciones, [estado], salario_min, salario_max, productos_lower)

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