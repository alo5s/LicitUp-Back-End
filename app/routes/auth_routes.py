from flask import Blueprint, jsonify, request
# Libreria para hash el password para el login
from werkzeug.security import generate_password_hash, check_password_hash
# Libreria para el token de login
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Model
from ..models.auth import AuthModel

auth_bp = Blueprint('auth',__name__)
# Alias para simplificar la escritura licitaciones
# li = licitaciones

@auth_bp.route("/register", methods=["POST"])
def registro_usuario():
    data = request.get_json()

    if not data or not all(key in data for key in ('email', 'password')):
        return jsonify({"message": "Faltan campos obligatorios"}), 200

    email = data['email']
    password = data['password']

    usuario_model = AuthModel()

    if usuario_model.usuario_existente(email):
        return {'message': 'El correo electrónico ya existe'}, 200

    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    user_entity = (email, password_hash)

    affected_rows = usuario_model.registrar_usuario(user_entity)

    if affected_rows > 0:
        # Token de acceso
        access_token = create_access_token(identity=email)
        return {'message': 'Usuario registrado exitosamente', 'access_token': access_token}, 201
    else:
        return {'message': 'La registración de usuario falló'}, 200

@auth_bp.route("/login", methods=["POST"])
def login_usuario():
    data = request.get_json()

    if not data or not all(key in data for key in ('email', 'password')):
        return {'message': 'Faltan campos obligatorios'}, 200

    email = data['email']
    password = data['password']

    usuario_model = AuthModel()
    stored_password_hash = usuario_model.obtener_contraseña(email)

    if stored_password_hash is None:
        return jsonify ({'message': 'Usuario no encontrado'}), 201

    if not check_password_hash(stored_password_hash, password):
        return jsonify ({'message': 'Contraseña inválida'}), 201

    access_token = create_access_token(identity=email)

    return jsonify(access_token=access_token), 200



# Ruta protegida para agregar elementos a favoritos (requiere token JWT)
@auth_bp.route("/add-favorite", methods=["POST"])
@jwt_required()
def agregar_favoritos():
    current_user = get_jwt_identity()
    data = request.get_json()
    item_to_add = data.get('item')
    
    affected_rows = AuthModel().add_favorito(item_to_add, current_user)
    if affected_rows > 0:
        return {'message': 'Siguiendo licitacion'}, 201
    else:
        return {'message': 'Falló en seguir licitacion'}, 200


# Ruta protegida para eleminar elementos a favoritos (requiere token JWT)
@auth_bp.route("/dalate-favorite", methods=["POST"])
@jwt_required()
def eliminar_favoritos():
    current_user = get_jwt_identity()
    data = request.get_json()
    item_to_add = data.get('item')
    
    affected_rows = AuthModel().delete_favorito(item_to_add, current_user)
    if affected_rows > 0:
        return {'message': 'Listo'}, 201
    else:
        return {'message': 'Falló en seguir licitacion'}, 200



# Ruta protegida de lista de favoritos del usario id_licitaciones (requiere token JWT)
@auth_bp.route("/lista-favorite-id", methods=["POST"])
@jwt_required()
def lst_favorito_id():
    try:
        current_user = get_jwt_identity()
        
        consulta = AuthModel().lista_id_favorito(current_user)
        data = []
        for row in consulta:
            formatted_row = {
                "fav_licitacion": row,
            }
            data.append(formatted_row)
        return jsonify({'lista_seguimiento': data}), 200
    except Exception as ex:
        return jsonify({'error': 'Error al obtener licitaciones: ' + str(ex)}), 500




