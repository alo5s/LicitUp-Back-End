# routes/home_routes.py

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
# Model
from ..models.home import HomeModel

home_bp = Blueprint('home', __name__)
# Alias para simplificar la escritura licitaciones
# li = licitaciones


@home_bp.route('/home',  methods=["POST"])
def li_count():
    try:
        # Obtener el conteo directamente sin necesidad de crear una instancia de HomeModel
        total_count = HomeModel().count()

        # Devolver la respuesta JSON directamente sin necesidad de una variable intermedia
        return jsonify({"total": total_count}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


