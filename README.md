# LicitUp Backend

Este es el backend de LicitUp, una aplicación web construida con Vue.js en el frontend y Flask API en el backend. Proporciona funcionalidades como registro de usuarios, inicio de sesión, análisis con suavizamiento exponencial para predecir productos, seguridad con JWT token, localización y un bot para conectarse a la API de Mercado Público.


## Uso
1. Inicia la aplicación: `python run.py`
2. Abre tu navegador y visita: `http://localhost:8080`


## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).


## Estructura del Proyecto

La estructura del proyecto es la siguiente:

```plaintext
/app
|-- database
|   |-- db1.py
|   |-- db.py
|   └── ModelSql.sql
|
|-- __init__.py
|-- __main__.py
|
|-- models
|   |-- auth.py
|   |-- home.py
|   |-- licitaciones.py
|   |-- mapa.py
|   |-- notification.py
|   |-- profile.py  # Nuevo
|   └── segumientos.py
|
|-- routes
|   |-- analisis_routes.py
|   |-- auth_routes.py
|   |-- home_routes.py
|   |-- licitaciones_routes.py
|   |-- mapa_routes.py
|   |-- notification_routes.py
|   |-- profile_routes.py  # Nuevo
|   └── segumientos_routes.py
|
|-- static
|   └── data.csv
|
|-- templates
|   └── plantilla_correo.html
|
|-- utils
|
|-- __init__.py
|-- __main__.py
|  
|
|-- README.md
|-- config.py
|-- data.csv
|-- picon.conf
|-- requirements.txt
|-- run.py
|-- test
└── env

