# routes/home_routes.py

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from datetime import datetime
from .. import cache # importar 'cache' desde el módulo principal
# Model
from ..models.home import HomeModel

home_bp = Blueprint('home', __name__)
# Alias para simplificar la escritura licitaciones
# li = licitaciones


@home_bp.route('/home',  methods=["POST"])
@cache.cached(timeout=60)  # Cachea la respuesta durante 60 segundos
def li_count():
    try:
        data = HomeModel().count()
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%d-%m-%y')

        # Devuelve una respuesta JSON con el resultado del conteo
        response_data = {
            "Fecha": fecha_formateada,
            "total": data
        }
        # response_data = "Esto es una prueba"
        return jsonify(response_data), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500