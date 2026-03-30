from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Cargar el modelo guardado al arrancar el servidor
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'modelo_precio_casa.joblib')

try:
    modelo_casas = joblib.load(model_path)
    print("====================================")
    print("Modelo de predicción de casas CARGADO")
    print("====================================")
except Exception as e:
    print(f"Advertencia: No se pudo cargar el modelo. Detalle: {e}\nPor favor, ejecuta primero 'proyecto_final_colab.py' para entrenar y guardar el modelo.")
    modelo_casas = None

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "api_name": "API de Predicción del Precio de la Vivienda (SalePrice) - Proyecto IA",
        "endpoints": {
            "/predict": "POST - Envia un JSON con los datos de una casa para recibir su precio estimado."
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not modelo_casas:
        return jsonify({"error": "El modelo no se encuentra disponible. Falta entrenarlo."}), 500
        
    try:
        data = request.get_json(force=True)
        # Parseamos el diccionario de entrada convirtiendolo en un DataFrame de pandas de 1 fila.
        # Es clave porque nuestro pipeline internamente espera el mismo formato con nombres de columna
        input_df = pd.DataFrame([data])
        
        # Realizamos la predicción con el pipeline que también se encarga del imputing y rescalado
        prediccion = modelo_casas.predict(input_df)[0]
        
        return jsonify({
            "status": "success",
            "precio_estimado_usd": round(float(prediccion), 2)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    # Lanzar el servidor de Flask
    app.run(host='0.0.0.0', port=5001, debug=True)
