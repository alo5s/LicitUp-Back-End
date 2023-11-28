import pandas as pd
import numpy as np
import json
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing
from flask import Blueprint, jsonify, request, Response
from datetime import datetime
import time
from .. import cache



analisis_bp = Blueprint('analisis',__name__)

# Cargar tus datos en un DataFrame de pandas
# df = pd.read_csv('data.csv')
# df = pd.read_csv('data.csv')
df = pd.read_csv('app/static/data.csv')

# el suavizamiento exponencial de Holt-Winters
def suavizadoExpHW(df):
    # Crear un diccionario para almacenar los resultados
    results = {}

    # Obtener la lista de productos únicos
    productos = df['producto'].unique()

    for producto in productos:
        producto_data = df[df['producto'] == producto].drop(columns=['producto'])

        # Reformatear los datos para que tengan una sola dimensión
        producto_data = producto_data.values.flatten()

        # Realizar el suavizamiento exponencial
        model = ExponentialSmoothing(producto_data, seasonal='add', seasonal_periods=12)
        model_fit = model.fit(optimized=True, use_boxcox=True)

        # Predecir los valores faltantes
        forecast = model_fit.forecast(steps=12)

        # Crear un diccionario con las predicciones
        forecast_dict = {month: int(value) for month, value in zip(df.columns[1:], forecast)}

        # Agregar el diccionario al resultado
        results[producto] = forecast_dict

    # Convertir los resultados a formato JSON al final de todas las iteraciones
    result_json = json.dumps(results, indent=4)
    return result_json

# suavizamiento exponencial simple
def suavizadoExpSES(df):
    results = {}
    productos = df['producto'].unique()

    for producto in productos:
        producto_data = df[df['producto'] == producto].drop(columns=['producto'])
        producto_data = producto_data.values.flatten()

        # Crear el modelo SES con optimización de parámetros
        model = SimpleExpSmoothing(producto_data)
        # Ajusta el valor de smoothing_level según sea necesario
        model_fit = model.fit(optimized=True, smoothing_level=0.1)
          
        # Predecir los valores faltantes
        forecast = model_fit.forecast(steps=12)

        # Agregar los valores directamente a la lista de resultados
        results[producto] = [int(value) for value in forecast]
        
        # Agregar ruido
        forecast_with_noise = [int(value + np.random.normal(scale=10)) for value in forecast]
        results[producto] = forecast_with_noise

    result_json = json.dumps(results, ensure_ascii=False, indent=4)
    return result_json

@analisis_bp.route("/analisis", methods=["GET"])
@cache.cached(timeout=600)  
def realizar_analisis():
    try:
        # resultados_exp_hw = suavizadoExpHW(df)
        resultados_exp_ses = suavizadoExpSES(df)
        # Establecer el tipo de contenido como "application/json"
        response = jsonify(json.loads(resultados_exp_ses))
        response.headers.add('Content-Type', 'application/json')
        return response, 200
    except Exception as ex:
        return jsonify({'error': 'Error al realizar el análisis: ' + str(ex)}), 500










