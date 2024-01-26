from dotenv import load_dotenv  # Instalar con pip install python-dotenv
import os

load_dotenv()  # Carga todo el contenido de .env en variables de entorno

class Config(object):
    DEBUG = False   
    SECRET_KEY =  os.environ.get('SECRET_KET_FLASK')
    DB_TOKEN = os.environ.get("DB_TOKEN", "") 
    ENCRYPT_DB = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

class ProductionConfig(Config):
    DEBUG = False
    
class DevelopmentConfig(Config):
    DEBUG = True 
    SERVER_NAME = "127.0.0.1:8000"
    #SERVER_NAME = "localhost:8000"
