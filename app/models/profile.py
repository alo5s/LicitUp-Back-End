# models/Profile.py


from ..database.db import get_db_connection   # la conexión de la base de dato

class ProfileModel:
    def listaComunaMapa():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                SELECT id, comunaunidad FROM ubicaciones 
                """
                cursor.execute(sql)
                data = cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return data

    def id_usario(correo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT id FROM usuarios WHERE correo = %s"
                cursor.execute(sql, (correo,))
                existing_user = cursor.fetchone()
                return existing_user[0] if existing_user else None
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
    
    def addDataPerfil(id_usuario, ls_1,ls_2, ls_3, numero_lis, monto_minimo, monto_maximo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:

                if ls_1:
                    sql_1 = """
                    INSERT INTO nombre_comuna_favorita (usuario_id, nombre_comuna) VALUES (%s, %s)
                    """
                    cursor.executemany(sql_1, [(id_usuario, i) for i in ls_1])

                if ls_2:
                    sql_2 = """
                    INSERT INTO nombre_producto_servicio_favorita (usuario_id, nombre_producto_servicio) VALUES (%s, %s)
                    """
                    cursor.executemany(sql_2, [(id_usuario, i) for i in ls_2])


                if ls_3:
                    sql_3 = """
                    INSERT INTO codificaciones_perfil (usuario_id, codificacio) VALUES (%s, %s)
                    """
                    cursor.executemany(sql_3, [(id_usuario, i) for i in ls_3])


                if numero_lis is not None and monto_minimo is not None and monto_maximo is not None:
                    sql_4 = """
                    INSERT INTO parametros_perfil (usuario_id, numero_licitacion, monto_min, monto_max) VALUES (%s, %s, %s, %s)
                    """
                    cursor.executemany(sql_4, [(id_usuario, numero_lis, monto_minimo, monto_maximo)])
                else:
                    print("Alguno de los valores es None o equivalente a False.")


                conn.commit()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
    
    @classmethod
    def transformar_datos_perfil(cls, data):
        datos = {
            "correo": data[0][0],
            "nLicitacion": set(),
            "Salario_max": set(),
            "Salario_min": set(),
            "codificaciones": set(),
            "ciudades": set(),
            "productos": set()
        }

        for row in data:
            nLicitacion = row[0]
            salario_min = row[1]
            salario_max = row[2]

            # Verificar si ya hemos agregado esta combinación
            if (nLicitacion, salario_min, salario_max) not in datos["nLicitacion"]:
                datos["nLicitacion"].add(nLicitacion)
                datos["Salario_min"].add(salario_min)
                datos["Salario_max"].add(salario_max)
                datos["codificaciones"].add(row[3])
                datos["ciudades"].add(row[5])   # Agregar el nombre de la ciudad
                datos["productos"].add(row[4])  # Agregar el nombre del producto

        return datos

    @classmethod
    def DataPerfil(cls, correo_usuario):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                SELECT DISTINCT
                    ppu.numero_licitacion,
                    MIN(ppu.monto_min) AS monto_min,
                    MAX(ppu.monto_max) AS monto_max,
                    ndcf.codificacio,
                    npsf.nombre_producto_servicio,
                    ncf.nombre_comuna
                FROM
                    usuarios u
                LEFT JOIN
                    parametros_perfil ppu ON u.id = ppu.usuario_id
                LEFT JOIN
                    codificaciones_perfil ndcf ON u.id = ndcf.usuario_id
                LEFT JOIN
                    nombre_producto_servicio_favorita npsf ON u.id = npsf.usuario_id
                LEFT JOIN
                    nombre_comuna_favorita ncf ON u.id = ncf.usuario_id
                WHERE
                    u.correo = %s
                GROUP BY
                    ppu.numero_licitacion,
                    ndcf.codificacio,
                    npsf.nombre_producto_servicio,
                    ncf.nombre_comuna;
                """
                cursor.execute(sql, (correo_usuario,))
                data = cursor.fetchall()

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()

        # Transformar datos utilizando la nueva función
        transformed_data = cls.transformar_datos_perfil(data)  # Cambiar 'self' a 'cls'
        return transformed_data

    @classmethod
    def Perfile_mapas(cls, correo_usuario):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                SELECT DISTINCT
                    ncf.nombre_comuna
                FROM
                    usuarios u
                LEFT JOIN
                    nombre_comuna_favorita ncf ON u.id = ncf.usuario_id
                WHERE
                    u.correo = %s;
                """
                cursor.execute(sql, (correo_usuario,))
                data = cursor.fetchall()

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return data

    @classmethod
    def borrar_dato_comuna(cls, correo_usuario,comuna):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                DELETE FROM nombre_comuna_favorita
                WHERE usuario_id = (
                    SELECT id
                    FROM usuarios
                    WHERE correo = %s
                ) AND nombre_comuna = %s;
                """
                cursor.execute(sql, (correo_usuario, comuna))
                conn.commit()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()


    @classmethod
    def borrar_dato_producto(cls, correo_usuario, producto):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                DELETE FROM nombre_producto_servicio_favorita
                WHERE usuario_id = (
                    SELECT id
                    FROM usuarios
                    WHERE correo = %s
                ) AND nombre_producto_servicio = %s;
                """
                cursor.execute(sql, (correo_usuario, producto))
                conn.commit()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()

    @classmethod
    def borrar_dato_codificacion(cls, correo_usuario, codificacion):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                DELETE FROM codificaciones_perfil
                WHERE usuario_id = (
                    SELECT id
                    FROM usuarios
                    WHERE correo = %s
                ) AND codificacio = %s;
                """
                cursor.execute(sql, (correo_usuario, codificacion))
                conn.commit()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()



    def updateDataPerfil(id_usuario, ls_1,ls_2, ls_3, numero_lis, monto_minimo, monto_maximo):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:

                # Actualizar nombre_comuna_favorita
                if ls_1:
                    sql_1_select = """
                        SELECT nombre_comuna
                        FROM nombre_comuna_favorita
                        WHERE usuario_id = %s
                    """
                    cursor.execute(sql_1_select, (id_usuario,))
                    existing_comunas = {row[0] for row in cursor.fetchall()}
                    nuevas_comunas = [(id_usuario, i) for i in ls_1 if i not in existing_comunas]
                    if nuevas_comunas:
                        sql_1_insert = """
                            INSERT INTO nombre_comuna_favorita (usuario_id, nombre_comuna)
                            VALUES (%s, %s)
                        """
                        cursor.executemany(sql_1_insert, nuevas_comunas)

                # Actualizar nombre_producto_servicio_favorita
                if ls_2:
                    sql_2_select = """
                        SELECT nombre_producto_servicio
                        FROM nombre_producto_servicio_favorita
                        WHERE usuario_id = %s
                    """
                    cursor.execute(sql_2_select, (id_usuario,))
                    existing_productos = {row[0] for row in cursor.fetchall()}
                    nuevos_productos = [(id_usuario, i) for i in ls_2 if i not in existing_productos]
                    if nuevos_productos:
                        sql_2_insert = """
                            INSERT INTO nombre_producto_servicio_favorita (usuario_id, nombre_producto_servicio)
                            VALUES (%s, %s)
                        """
                        cursor.executemany(sql_2_insert, nuevos_productos)

                # Actualizar codificaciones_perfil
                if ls_3:
                    sql_3_select = """
                        SELECT codificacio
                        FROM codificaciones_perfil
                        WHERE usuario_id = %s
                    """
                    cursor.execute(sql_3_select, (id_usuario,))
                    existing_codificaciones = {row[0] for row in cursor.fetchall()}
                    nuevas_codificaciones = [(id_usuario, i) for i in ls_3 if i not in existing_codificaciones]
                    if nuevas_codificaciones:
                        sql_3_insert = """
                            INSERT INTO codificaciones_perfil (usuario_id, codificacio)
                           VALUES (%s, %s)
                        """
                        cursor.executemany(sql_3_insert, nuevas_codificaciones)

                # Actualizar parametros_perfil
                if numero_lis is not None or monto_minimo is not None or monto_maximo is not None:
                    sql_4 = """
                        UPDATE parametros_perfil
                        SET 
                            monto_min = COALESCE(%s, monto_min),
                            monto_max = COALESCE(%s, monto_max),
                            numero_licitacion = COALESCE(%s, numero_licitacion)
                        WHERE usuario_id = %s;
                    """
                    cursor.execute(sql_4, (monto_minimo, monto_maximo, numero_lis, id_usuario))

                conn.commit()
        except Exception as ex:
            print(f"Error en updateDataPerfil: {ex}")
            raise Exception(ex)
        finally:
            conn.close()








