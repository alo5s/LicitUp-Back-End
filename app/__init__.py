# app/__init__.py

from flask import Flask
from datetime import timedelta
from config import *
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache

#app = Flask(__name__, template_folder='/app/static/')
app = Flask(__name__)

app.config.from_object(ProductionConfig)

# Inicializa el JWTManager
jwt = JWTManager(app)

# Configura CORS para permitir solicitudes desde el cliente (Front-end)

CORS(app, resources={r"/api/v1/*": {"origins": ["http://localhost:5173", "https://licitup-x69i.onrender.com"]}})

# Inicializa la caché
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


# CORS = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
 
# CORS = CORS(app,  resources={r"/*": {"origins": "https://licitup-1.onrender.com"}})

# La duración máxima del token en 30 días
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Registro de las rutas definidas en el blueprint
from .routes import *
app.register_blueprint(home_bp, url_prefix='/api/v1/')
app.register_blueprint(licitaciones_bp, url_prefix='/api/v1/')
app.register_blueprint(auth_bp, url_prefix='/api/v1/')
app.register_blueprint(segumientos_bp, url_prefix='/api/v1/')
app.register_blueprint(mapa_bp, url_prefix='/api/v1/')
app.register_blueprint(analisis_bp, url_prefix='/api/v1/')
app.register_blueprint(profile_bp, url_prefix='/api/v1/')


app.register_blueprint(notification_bp, url_prefix='/api/v1/')


# admins
app.register_blueprint(admin_bp, url_prefix='/api/v1/')
