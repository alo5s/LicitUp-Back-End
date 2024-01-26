# routes/admin_routes.py
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from datetime import datetime
from .. import cache # importar 'cache' desde el módulo principal
# Model
from ..models.home import HomeModel, AdminModel

admin_bp = Blueprint('admin', __name__)
# Alias para simplificar la escritura licitaciones
# li = licitaciones

@admin_bp.route('/admin',  methods=["POST"])
@cache.cached(timeout=60)  # Cachea la respuesta durante 60 segundos
def lst_usuarios():
    try:
        data = AdminModel().ls_usuario()  # Agrega paréntesis para llamar al método

        # Devuelve una respuesta JSON con el resultado del conteo
        response_data = [{"correo": row[0], "suscripcion": row[1]} for row in data]
        return jsonify(response_data), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500



@admin_bp.route('/admin/activar',  methods=["POST"])
def usuario():
    data = request.json 
    correo = data.get('correo')
    suscripcion = data.get('suscripcion')
    
    affected_rows = AdminModel().update_suscripcion(correo, suscripcion)
    if affected_rows > 0:
        return {'message': 'Listo'}, 201
    else:
        return {'message': 'Falló'}, 200



@admin_bp.route("/admin/estado", methods=["POST"])
@cache.cached(timeout=60)
@jwt_required()
def estado():
    try:
        current_user = get_jwt_identity()
        print(current_user)
        estado = AdminModel().usario_estado(current_user)
        response_data = {
            'estado': estado  
        }
        return jsonify(response_data), 200
    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500