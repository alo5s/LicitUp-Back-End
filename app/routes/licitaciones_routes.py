# routes/licitaciones_routes.py

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from datetime import datetime
from .. import cache
# Model
from ..models.licitaciones import LicitacionesModel
from ..models.profile import ProfileModel

licitaciones_bp = Blueprint('licitaciones', __name__)
# Alias para simplificar la escritura licitaciones
# li = licitaciones

# Esto fundion recive un palabbra y return el valor del dicci
def estado_str(estado):
    estados = {
        'Todo': None, 
        'Publicada': 5,
        'Cerrada': 6,
        'Desierta': 7,
        'Adjudicada': 8,
        'Revocada': 19
    }
    return estados.get(estado, None)

# Esto fundion recive un nuemero y return el valor del dicci
def estado_int(estado):
    estados = {
        None: 'Todo',
        5: 'Publicada',
        6: 'Cerrada',
        7: 'Desierta',
        8: 'Adjudicada',
        19: 'Revocada'
    }

    return estados.get(estado, None)

# Función para formatear la fecha
def formatear_fecha(fecha_str):
    try:
        fecha_objeto = datetime.strptime(fecha_str, "%a, %d %b %Y %H:%M:%S GMT")
        return fecha_objeto.strftime("%d-%m-%Y %H:%M:%S")
    except ValueError:
        return None

@licitaciones_bp.route("/licit",  methods=["POST"])  
def listar_licitaciones():
    try:
        data = request.json  # Obtiene los datos del cuerpo de la solicitud en formato JSON
        pagina = data.get('pagina', 1)
        elementos_por_pagina = int(data.get('elementos_por_pagina', 35))
        estado = data.get('estado')
        fecha_final = data.get('fecha_inicial', None) 
        fecha_inicial = data.get('fecha_final', None) 
        orden = data.get("formato_ordende", None)
        # Estado el codigo numerico
        estado_numerico = estado_str(estado)
        print(f"feha inicial {fecha_inicial}")
        print(f"fecha fin {fecha_final}")
        consulta, total_registros, total_licitaciones = LicitacionesModel().ts_2(pagina, elementos_por_pagina, estado_numerico, fecha_inicial, fecha_final, orden)
        data = []
        for row in consulta:
            formatted_row = {
                "id_licitacion": row[0],
                "Estado": estado_int(int(row[2])),               
                "CodigoExterno": row[1],
                "Descriptive_name": row[3],
                "fecha": formatear_fecha(row[4].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[4] else None
            }
            data.append(formatted_row)

        # Calcula el número total de páginas
        # print("total de licitacion :", total_licitaciones)
        # print(data)
        total_paginas = -(-total_registros // elementos_por_pagina)  # Divide redondeando hacia arriba
        return jsonify({'licitaciones_pagina': data, 'total_paginas': total_paginas, "total_licitaciones": total_licitaciones }), 200

    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500



@licitaciones_bp.route("/buscar", methods=["POST"])
def buscar_licitaciones():
    try:
        data = request.json  # Obtiene los datos del cuerpo de la solicitud en formato JSON
        txt_data = data.get('buscar')
        
        # Verificar si el primer elemento es un número
        if txt_data and txt_data[0].isdigit():
            codigo_externo = txt_data
            descriptive_name = None
        else:
            codigo_externo = None
            descriptive_name = txt_data

        # Realizar la búsqueda en la base de datos según corresponda
       
        consulta, total_licitaciones = LicitacionesModel().srec(descriptive_name, codigo_externo)
        print("total de licitacion :", total_licitaciones)
        data = []
        
        for row in consulta:
            formatted_row = {
                "id_licitacion": row[0],
                "Estado": estado_int(int(row[2])),               
                "CodigoExterno": row[1],
                "Descriptive_name": row[3],
                "fecha": formatear_fecha(row[4].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[4] else None
            }
            data.append(formatted_row)

        return jsonify({'licitaciones_pagina': data,"total_licitaciones": total_licitaciones}), 200

    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 200


@licitaciones_bp.route('/licitaciones/detalle=<int:id>', methods=['POST'])
@cache.cached(timeout=600)   
def licitaciones_datos_info(id):
    row = LicitacionesModel().detalle(id)
    data = {
        "CodigoExterno": row[0],
        "Estado": estado_int(int(row[1])),
        "Descriptive_name": row[2],
        "Nombre_del_Organismo": row[3],
        "Producto": row[4],
        "Precio": row[5],
        "Cantidad": row[6],
        "FechaCreacion": formatear_fecha(row[7].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[7] else None,
        "FechaPublicacion": formatear_fecha(row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[8] else None,
        "FechaCerrada": formatear_fecha(row[9].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[9] else None,
        "FechaDesierta": formatear_fecha(row[10].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[10] else None,
        "FechaRevocada": formatear_fecha(row[11].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[11] else None,
        "FechaSuspendido": formatear_fecha(row[12].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[12] else None,
        "FechaAdjudicacion": formatear_fecha(row[13].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[13] else None,
        "ComunaUnidad": row[14],
        "FechaInicio": formatear_fecha(row[15].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[15] else None,
        "FechaFinal": formatear_fecha(row[16].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[16] else None,
        "FechaPubRespuestas": formatear_fecha(row[17].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[17] else None, 
        }
    
    return jsonify({'detalle_li': data}), 200







from flask import abort


# LISITACIONE DE USARIO LOGIADOS, CON SUS PARAMETREO
# Endpoind Datos del Usuario
@licitaciones_bp.route('/licitaciones/perfil',  methods=["POST"])
@jwt_required()
def asd_data_profile():
    """
    Endpoint para obtener los licitaciones de preferencia del usuario, etc.
    """
    try:
        # Obtiene los datos del cuerpo de la solicitud en formato JSON
        data = request.json  
        pagina = data.get('pagina', 1)
        # Obtener datos del perfil
        current_user = get_jwt_identity()
        parametro_perfil = ProfileModel.DataPerfil(current_user)

        consulta, total_licitaciones = LicitacionesModel().licitaciones_perfil(parametro_perfil, pagina)
    
        total_registros = len(consulta)
        
        data = []
        for row in consulta:
            formatted_row = {
                "id_licitacion": row[0],
                "Estado": estado_int(int(row[2])),               
                "CodigoExterno": row[1],
                "Descriptive_name": row[3],
                "fecha": formatear_fecha(row[4].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[4] else None
            }
            data.append(formatted_row)

        # Calcula el número total de páginas
        total_paginas = -(-total_registros // 35)  # Divide redondeando hacia arriba
        return jsonify({'licitaciones_pagina': data, 'total_paginas': total_paginas, "total_licitaciones": total_licitaciones}), 200

    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500