from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from datetime import datetime
from .. import cache

# Model
from ..models.mapa import MapaModel
from ..models.profile import ProfileModel
from ..models.licitaciones import LicitacionesModel

mapa_bp = Blueprint('mapa', __name__)
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


@mapa_bp.route('/mapa',  methods=["GET"])
@cache.cached(timeout=600)  # Cachea durante 10 minutos
def mapa():
    try:
        consulta = MapaModel.mapa()
        coordenadas_ciudades = []
        for resultado in consulta:
            ciudad_id, nombre_ciudad, cantidad, latitud, longitud = resultado
            coordenadas_ciudades.append({
                "id": ciudad_id,
                "ciudad": nombre_ciudad,
                "Cantidad": cantidad,
                "coordenada": {
                    "latitud": latitud,
                    "longitud": longitud
                }
            })
        return jsonify(coordenadas_ciudades), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    
@mapa_bp.route('/mapa/licitaciones/<id>/pagina=<int:page>',  methods=["GET"])
def mapa_licitaciones(id, page):
    try:
        # Obtén el número de página de la consulta desde la URL
        page = int(request.args.get('page', 1))
        items_per_page = int(request.args.get('items_per_page', 25))

        # Llama a la función para obtener las licitaciones por ubicación con paginación
        licitaciones, total_registros = MapaModel().obtener_licitaciones_por_ubicacion(id, page, items_per_page)

        data = []

        for row in licitaciones:
            formatted_row = {
                "id_licitacion": row[0],
                "Estado": estado_int(int(row[2])),               
                "CodigoExterno": row[1],
                "Descriptive_name": row[3],
                "fecha": formatear_fecha(row[4].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[4] else None
            }
            data.append(formatted_row)

        # Calcula el número total de páginas
        total_paginas = -(-total_registros // items_per_page)  # Divide redondeando hacia arriba
        return jsonify({'licitaciones_pagina': data, 'total_paginas': total_paginas})
    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones por ubicación: ' + str(ex)}), 500




@mapa_bp.route('/perfil/mapas',  methods=["POST"])
@jwt_required()
def mapas_profere():
    try:
        # Obtener datos del perfil
        current_user = get_jwt_identity()
        parametro_perfil = ProfileModel.Perfile_mapas(current_user)
        
        # Obtiener las mapas
        consulta = MapaModel.mapa_usuario(parametro_perfil)
        coordenadas_ciudades = []
        for resultado in consulta:
            ciudad_id, nombre_ciudad, latitud, longitud = resultado
            coordenadas_ciudades.append({
                "id": ciudad_id,
                "ciudad": nombre_ciudad,
                "coordenada": {
                    "latitud": latitud,
                    "longitud": longitud
                }
            })
        return jsonify(coordenadas_ciudades), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500




# LISITACIONE UBICACION MAPA DE USARIO LOGIADOS, CON SUS PARAMETREO
# Endpoind Datos del Usuario

@mapa_bp.route('/licitaciones/perfil/mapa',  methods=["POST"])
@jwt_required()
def asd_data_profile():
    """
    Endpoint para obtener los licitaciones de preferencia del usuario, etc.
    """
    try:
        # Obtiene los datos del cuerpo de la solicitud en formato JSON  Las Cabras
        data = request.json  
        pagina = data.get('pagina', 1)
        comuna = data.get('comuna')
        print(comuna)
        # Obtener datos del perfil
        current_user = get_jwt_identity()
        parametro_perfil = ProfileModel.DataPerfil(current_user)
        
        consulta = MapaModel.licitaciones_perfil_mapa(parametro_perfil, pagina, comuna)
        
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
        return jsonify({'licitaciones_pagina': data, 'total_paginas': total_paginas}), 200

    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500