from flask import Blueprint, jsonify, request, Response, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv 
from datetime import datetime

import os
import smtplib
import time
import json
# Libreria para hash el password para el login
from werkzeug.security import generate_password_hash, check_password_hash
# Libreria para el token de login
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Model
from ..models.notification import NotificationModel

notification_bp = Blueprint('notification',__name__)

load_dotenv()  # Carga todo el contenido de .env en variables de entorno


# Esta confiutado con un json conecar a la api
def licitacionesApi():
    # Ruta al archivo JSON con los datos
    json_file = "test/datos.json"

    # Abre el archivo JSON con codificación UTF-8
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    datos = []
    for item in data:
        codigo_externo = item.get("CodigoExterno", "")
        codigo_estado = item.get("CodigoEstado", "")
        # fechas = "2023-10-29 10:00:00+00"
        
        datos.append({
            "codigo_externo": codigo_externo,
            "codigo_estado": codigo_estado,
            # "fechas": fechas
        })
    
    return datos

def comprobar(licitaciones_db, licitaciones_chile):
    notificaciones = []

    for db_licitacion in licitaciones_db:
        db_codigo_externo = db_licitacion[0]
        db_codigo_estado = db_licitacion[1]

        matching_licitacion = next(
            (chile_licitacion for chile_licitacion in licitaciones_chile if chile_licitacion["codigo_externo"] == db_codigo_externo), None)

        if matching_licitacion:
            chile_codigo_estado = matching_licitacion["codigo_estado"]

            if db_codigo_estado != chile_codigo_estado:
                notificaciones.append({
                    "CodigoExterno": db_codigo_externo,
                    "CodigoEstadoDB": db_codigo_estado,
                    "CodigoEstadoNuevo": chile_codigo_estado
                })

    return notificaciones



def notificacion_usuarios_datos(licitacion):
    usarias_notifacar_datos = []  # Inicializa como una lista vacía
    for i in licitacion:
        if int(i["CodigoEstadoDB"]) is not int(i["CodigoEstadoNuevo"]):
            comprobador = NotificationModel().segumientos_comprobar_segumiento(i["CodigoExterno"])
            # actualizar_liciaciones = "Actualizar"
            if comprobador:
                usuario_data = NotificationModel().segumientos_datos_usario(comprobador)
                usarias_notifacar_datos.extend(usuario_data)  # Agrega datos a la lista
    
    return usarias_notifacar_datos






def enviar_correo(destinatario):
    # Configuración servidor de correo (para Gmail)
    #servidor_correo = "smtp.gmail.com"
    servidor_correo = "aspmx.l.google.com"
    puerto = 25
    usuario = os.environ.get('CORREO_SMTP')
    contraseña = os.environ.get('PASSWORD_SMTP')

    # Configurar el mensaje de correo
    mensaje = MIMEMultipart()
    mensaje['From'] = usuario
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Notificación"

    # Cuerpo del mensaje utilizando la plantilla HTML
    #xplantilla_html = '/templates/plantilla_correo.html'
    #cuerpo_mensaje = render_template(plantilla_html)
    #mensaje.attach(MIMEText(cuerpo_mensaje, 'html'))
    #cuerpo_mensaje = "#"
    mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

    # Establecer la conexión con el servidor de correo
    with smtplib.SMTP(servidor_correo, puerto) as servidor:
        servidor.starttls()  # Iniciar conexión segura
        servidor.login(usuario, contraseña)
        texto_mensaje = mensaje.as_string()
        servidor.sendmail(usuario, destinatario, texto_mensaje)



@notification_bp.route("/notificacion", methods=["POST"])
@jwt_required()
def main():
    licitaciones_db = NotificationModel().licitaciones()
    licitaciones_chile = licitacionesApi()
        
    # Función para comprobar las licitaciones
    datos_comprobar = comprobar(licitaciones_db, licitaciones_chile)

    # Función para obtener notificaciones y actualizar datos
    datos_usuarios = notificacion_usuarios_datos(datos_comprobar)
    id_usario_correo = get_jwt_identity()
    # Lógica para enviar notificaciones a usuarios autenticados
    alerta = False

    if datos_usuarios:
        for i in datos_usuarios:
            if id_usario_correo == i[1]:
                alerta = True
                return jsonify({'notificacion_activa': alerta})
    return jsonify({'notificacion_activa': alerta})















# Evento SSE tiene que ser si o si un dominio
#from app import app
#import json
#
#def event_notifacion():
#    count = 0
#    while True:
#        data = {'message': 'Nueva Estado'}
#        yield f"data: {json.dumps(data)}\n\n"  # Utiliza json.dumps en lugar de jsonify
#        print("Evento activo")
#        time.sleep(10)  # Simula actualizaciones periódicas
#
#
## Ruta para establecer la conexión SSE Para la Notificacion
#@segumientos_bp.route('/events')
#@jwt_required()
#def sse():
#    user_id = get_jwt_identity()
#    if user_id is not None:
#        activada = activate_notification(user_id)
#        
#    return Response(event_stream(), content_type='text/event-stream')