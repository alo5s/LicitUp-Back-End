from flask import Blueprint, jsonify, request, Response
from datetime import datetime
import time

# Libreria para hash el password para el login
from werkzeug.security import generate_password_hash, check_password_hash
# Libreria para el token de login
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# Model
from ..models.segumientos import SegumientosModel

segumientos_bp = Blueprint('segumientos',__name__)
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

# Esta funcion es para la retunre un volor de esta de ornde de compra
def estado_or(numero):
    estados = {
        4: "Enviada a Proveedor",
        5: "En proceso",
        6: "Aceptada",
        9: "Cancelada",
        12: "Recepción Conforme",
        13: "Pendiente de Recepcionar",
        14: "Recepcionada Parcialmente",
        15: "Recepcion Conforme Incompleta"
    }
    return estados.get(numero, None)

# Función para formatear la fecha
def formatear_fecha(fecha_str):
    try:
        fecha_objeto = datetime.strptime(fecha_str, "%a, %d %b %Y %H:%M:%S GMT")
        return fecha_objeto.strftime("%d-%m-%Y %H:%M:%S")
    except ValueError:
        return None





#@segumientos_bp.route("/segumientos", methods=["POST"])
#@jwt_required()
#def lst_favorito_id():
#    try:
#        current_user = get_jwt_identity()
#        consulta = SegumientosModel().licitaciones_segumientos(current_user)
#        licitationes = []
#        for row in consulta:
#            formatted_row = {
#                "CodigoExterno": row[0],
#                "Estado": estado_int(int(row[1])),
#                "Descriptive_name": row[2],
#                "Nombre_del_Organismo": row[3],
#                "Producto": row[4],
#                "Precio": row[5],
#                "Cantidad": row[6],
#                "FechaCreacion": formatear_fecha(row[7].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[7] else None,
#                "FechaPublicacion": formatear_fecha(row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[8] else None,
#                "FechaCerrada": formatear_fecha(row[9].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[9] else None,
#                "FechaDesierta": formatear_fecha(row[10].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[10] else None,
#                "FechaRevocada": formatear_fecha(row[11].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[11] else None,
#                "FechaSuspendido": formatear_fecha(row[12].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[12] else None,
#                "FechaAdjudicacion": formatear_fecha(row[13].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[13] else None,
#                "ComunaUnidad": row[14],
#            }
#            licitationes.append(formatted_row)
#        return jsonify({'licitationes': licitationes, 'orden_de_compra': orden_de_compra}), 200
#    except Exception as ex:
#        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500




#@segumientos_bp.route("/segumientos", methods=["POST"])
#@jwt_required()
#def lst_favorito_id():
#    try:
#        current_user = get_jwt_identity()
#        consulta = SegumientosModel().licitaciones_segumientos(current_user)
#        resultado = {'licitaciones': [], 'ordenes_de_compra': []}
#        
#        for row in consulta:
#            licitacion = {
#                "CodigoExterno": row[1],
#                "Estado": estado_int(int(row[2])),
#                "Descriptive_name": row[3],
#                "Nombre_del_Organismo": row[4],
#                "Producto": row[5],
#                "Precio": float(row[6]) if row[6] is not None else None,
#                "Cantidad": row[7],
#                "FechaCreacion": formatear_fecha(row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[8] else None,
#                "FechaPublicacion": formatear_fecha(row[9].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[9] else None,
#                "FechaCerrada": formatear_fecha(row[10].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[10] else None,
#                "FechaDesierta": formatear_fecha(row[11].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[11] else None,
#                "FechaRevocada": formatear_fecha(row[12].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[12] else None,
#                "FechaSuspendido": formatear_fecha(row[13].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[13] else None,
#                "FechaAdjudicacion": formatear_fecha(row[14].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[14] else None,
#                "ComunaUnidad": row[15],
#                "id_orden_compra": row[16]
#            }
#            resultado['licitaciones'].append(licitacion)
#            
#            if row[16] is not None:
#                orden_de_compra = {
#                    "id": row[16],
#                    "CodigoExterno": row[1],  # Puedes querer mostrar el CodigoExterno de la licitación relacionada
#                    "Estado": estado_int(int(row[2])),
#                    "Descriptive_name": row[3],
#                }
#                resultado['ordenes_de_compra'].append(orden_de_compra)
#
#        return jsonify(resultado), 200
#    except Exception as ex:
#        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500


@segumientos_bp.route("/segumientos", methods=["POST"])
@jwt_required()
def lst_favorito_id():
    try:
        current_user = get_jwt_identity()
        consulta = SegumientosModel().licitaciones_segumientos(current_user)
        licitaciones = []
        ordenes_de_compra = []
        for row in consulta:
            formatted_row = {
                "CodigoExterno": row[1],
                "Estado": estado_int(int(row[2])),
                "Descriptive_name": row[3],
                "Nombre_del_Organismo": row[4],
                "Producto": row[5],
                "Precio": float(row[6]),  # Convertir a flotante si es necesario
                "Cantidad": row[7],
                "FechaCreacion": formatear_fecha(row[8].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[8] else None,
                "FechaPublicacion": formatear_fecha(row[9].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[9] else None,
                "FechaCerrada": formatear_fecha(row[10].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[10] else None,
                "FechaDesierta": formatear_fecha(row[11].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[11] else None,
                "FechaRevocada": formatear_fecha(row[12].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[12] else None,
                "FechaSuspendido": formatear_fecha(row[13].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[13] else None,
                "FechaAdjudicacion": formatear_fecha(row[14].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[14] else None,
                "ComunaUnidad": row[15],
                "FechaInicio": formatear_fecha(row[16].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[15] else None,
                "FechaFinal": formatear_fecha(row[17].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[16] else None,
                "FechaPubRespuestas": formatear_fecha(row[18].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[17] else None, 
                "id_orden_compra": row[19]
            }
            licitaciones.append(formatted_row)
            # Si hay una orden de compra asociada, también la agregamos a la lista
            if row[20] is not None:
                orden_de_compra = {
                    "id": row[19],
                    "CodigoExterno": row[21],  # CodigoExterno de la licitación relacionada
                    "Estado": estado_or(int(row[22])),
                    "Descriptive_name": row[23],
                    "Nombre_del_Organismo": row[20],
                    "FechaCreacion": formatear_fecha(row[21].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[21] else None,
                    "FechaEnvio": formatear_fecha(row[22].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[22] else None,
                    "FechaAceptacion": formatear_fecha(row[23].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[23] else None,
                    "FechaCancelacion": formatear_fecha(row[24].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[24] else None,
                    "FechaUltimaModificacion": formatear_fecha(row[25].strftime("%a, %d %b %Y %H:%M:%S GMT")) if row[25] else None
                }
                ordenes_de_compra.append(orden_de_compra)

        return jsonify({'licitaciones': licitaciones, 'ordenes_de_compra': ordenes_de_compra}), 200
    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500



# Ruta protegida para eleminar elementos a favoritos (requiere token JWT)
@segumientos_bp.route("/segumientos/dalate", methods=["POST"])
@jwt_required()
def eliminar_favoritos():
    current_user = get_jwt_identity()
    data = request.get_json()
    item_to_dalete = data.get('item')
    
    affected_rows = SegumientosModel().licitaciones_segumientos_delete(item_to_dalete, current_user)
    if affected_rows > 0:
        return {'message': 'Listo'}, 201
    else:
        return {'message': 'Falló en seguir licitacion'}, 200






# Prueba evento SSE

from app import app
import json
#def event_stream():
#    count = 0
#    while True:
#        data = {'message': 'Datos de evento en tiempo adfsadf'}
#        yield f"data: {json.dumps(data)}\n\n"  # Utiliza json.dumps en lugar de jsonify
#        print("Evento activo")
#        time.sleep(5)  # Simula actualizaciones periódicas
#
#
## Ruta para establecer la conexión SSE
#@segumientos_bp.route('/events')
#def sse():
#    return Response(event_stream(), content_type='text/event-stream')

