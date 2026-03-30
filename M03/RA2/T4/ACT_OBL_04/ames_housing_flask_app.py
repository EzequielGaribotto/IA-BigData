from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__)) # Cargamos el modelo desde la carpeta 'model' dentro del directorio actual del script
model_path = os.path.join(current_dir, 'model', 'modelo_precio_casa.joblib')

try:
    modelo_casas = joblib.load(model_path)
    feature_columns = modelo_casas.feature_names_in_

except Exception as e:
    print(f"Error cargando modelo: {e}")
    modelo_casas = None
    feature_columns = None


def build_input(data: dict, feature_columns):
    df = pd.DataFrame([data])

    # Añadir columnas faltantes con NaN - Luego los Imputers del pipeline se encargarán de cambiar esos NaN por valores adecuados
    for col in feature_columns:
        if col not in df.columns:
            df[col] = np.nan

    return df[feature_columns]


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "message": "API de predicción de precios de casas en Ames, Iowa",
        "expected_features_a": list(feature_columns) if feature_columns is not None else "Modelo no disponible"
    })


@app.route('/predict', methods=['POST'])
def predict():
    if modelo_casas is None:
        return jsonify({"error": "Modelo no disponible"}), 500

    try:
        data = request.get_json(force=True)

        input_df = build_input(data, feature_columns)

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
    app.run(host='0.0.0.0', port=5001, debug=True)