from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from datetime import datetime
from .. import cache
# Model
from ..models.profile import ProfileModel

profile_bp = Blueprint('profile', __name__)


# Endpoind Datos del cuestionar para el perfil de usario
@profile_bp.route('/cuestionario',  methods=["GET"])
@cache.cached(timeout=600)  
def datacustionaro():
    """
    Endpoint para obtener lo que necesito el clien para el cuestionario del perfil de usuario.
    """
    try:
        consulta = ProfileModel.listaComunaMapa()
        # Utilizar comprensión de listas para construir el formato de respuesta
        dato = [{"id": ciudad_id, "ciudad": nombre_ciudad} for ciudad_id, nombre_ciudad in consulta]
        return jsonify({'comunas': dato}), 200
    except SomeSpecificException as ex:
        # Manejar excepciones específicas y devolver un código de estado HTTP apropiado
        abort(500, description=str(ex))


@profile_bp.route('/profile/datos',  methods=["POST"])
@cache.cached(timeout=600)  
@jwt_required()
def post_profile_datos():
    """
    Endpoint para procesar los datos del cuestionario del perfil de usuario enviados por el cliente.
    """
    try:
        current_user = get_jwt_identity()
        id_usario = ProfileModel.id_usario(current_user)
        
        # Este es data del cliente
        data = request.get_json()
        
        # Lista de comunas 
        ls_comuna = data['ls_comuna_fa']
        # Lista de producto o servicio
        ls_ps_ss = data['ls_PsSs_fa']
        # Lista de codificaciónes
        ls_codificacións = data['ls_codificacións_fa']
        # Otros Paramatremos
        numero_lis, monto_minimo, monto_maximo = data['ls_parametos'].values()


        print(numero_lis)
        # Guardar datos
        insertaDatosPerfil = ProfileModel.addDataPerfil(id_usario, ls_comuna, ls_ps_ss, ls_codificacións, numero_lis, monto_minimo, monto_maximo)

        # Asegurarse de que se han proporcionado datos
        if not data:
            abort(400, description="No se proporcionaron datos en la solicitud.")
        print(current_user)
        return jsonify({"message": "Datos Guardados correctamente"}), 200
    except Exception as ex:
        # Manejar excepciones generales y devolver un código de estado HTTP apropiado
        abort(500, description=str(ex))






@profile_bp.route('/perfil',  methods=["GET"])
@jwt_required()
def data_profile():
    """
    Endpoint para obtener los datos del usuario, etc.
    """
    try:
        current_user = get_jwt_identity()

        # Obtener datos del perfil
        consulta = ProfileModel.DataPerfil(current_user)

        # Construir formato de respuesta
        datos_perfil = {
            'correo': current_user,
            'nLicitacion': float(list(consulta['nLicitacion'])[0]),
            'Salario_max': float(list(consulta['Salario_max'])[0]),
            'Salario_min': float(list(consulta['Salario_min'])[0]),
            'ciudades': list(consulta['ciudades']),
            'productos': list(consulta['productos']),
            'codificacio': list(consulta['codificaciones']),

        }
        # Retornar un JSON con los datos del perfil
        return jsonify({'perfil': datos_perfil}), 200
    except Exception as ex:
        # Manejar excepciones generales y devolver un código de estado HTTP apropiado
        abort(500, description=str(ex))



@profile_bp.route('/perfil/borrar_dato', methods=['DELETE'])
@jwt_required()
def borrar_dato_perfil():
    try:
        current_user = get_jwt_identity()

        # Obtén el dato a borrar desde los parámetros de la solicitud
        dato_comuna = request.args.get('comuna', None)

        if dato_comuna is not None:
            ProfileModel.borrar_dato_comuna(current_user, dato_comuna)

        # Obtén la codificación del dato a borrar desde los parámetros de la solicitud
        data_codificacion = request.args.get("codificacion", None)
        if data_codificacion is not None:
            ProfileModel.borrar_dato_codificacion(current_user, data_codificacion)

        # Obtén el producto/servicio del dato a borrar desde los parámetros de la solicitud
        data_producto = request.args.get("producto_servicio", None)
        if data_producto is not None:
            ProfileModel.borrar_dato_producto(current_user, data_producto)

        return jsonify({'mensaje': 'Dato borrado exitosamente'})

    except Exception as e:
        print(f"Error en la función borrar_dato_perfil: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500





@profile_bp.route('/perfil/datos/update', methods=['PUT'])
@jwt_required()
def actualizar_datos():
    try:
        current_user = get_jwt_identity()
        id_usario = ProfileModel.id_usario(current_user)
        
        # Obtener los nuevos datos del cuerpo de la solicitud
        data = request.get_json()
        
        # Lista de comunas 
        ls_comuna = data['ls_comuna_fa']
        # Lista de producto o servicio
        ls_ps_ss = data['ls_PsSs_fa']
        # Lista de codificaciónes
        ls_codificacións = data['ls_codificacións_fa']
        # Otros Paramatremos
        numero_lis, monto_minimo, monto_maximo = data['ls_parametos'].values()

        update_insert = ProfileModel.updateDataPerfil(id_usario, ls_comuna, ls_ps_ss, ls_codificacións, numero_lis, monto_minimo, monto_maximo)
        return jsonify({'mensaje': 'Datos actualizados correctamente'}), 200
    except Exception as e:
        # Manejar cualquier error inesperado y devolver un código de estado 500 Internal Server Error
        return jsonify({'error': 'Error interno del servidor', 'detalle': str(e)}), 500