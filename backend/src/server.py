from flask import Flask, jsonify, request
from waitress import serve
from flask_cors import CORS
import logging
import requests
from keras.models import load_model
from sklearn.preprocessing import StandardScaler,OneHotEncoder
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
# Setting up a Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Setting up a GPT model API key (placeholder)
apiKey = "your_api_key"

#loading the model
model = load_model('backend/src/house_price_prediction_model.h5')


numerical_features = ['bed', 'bath', 'acre_lot', 'house_size','zip_code','street']
categorical_features = ['city', 'state']

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder()

#price trent for individual property
@app.route('/api/v1/price-trend/individual-property/<property_id>', methods=['GET'])
def individual_property_price_trend(property_id):
    try:
        # Here you would call your GPT model or database to get the price trend
        # For now, we return a placeholder message
        price_trend = f"Single Property Price {property_id}"
        return jsonify(message=price_trend), 200
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#getting geospatial information of the given latitude and longitude
@app.route('/api/v1/geospatial/<lat>/<lng>/<type>', methods=['GET'])
def geospatial(lat,lng, type):
    try:
        url = 'https://places.googleapis.com/v1/places:searchNearby'
        data = {
    "includedTypes": ["liquor_store", "convenience_store"],
    "maxResultCount": 10,
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": 37.7937,
                "longitude": -122.3965
            },
            "radius": 1000.0
        }
    }
}
        headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': 'AIzaSyAvamq-1AR2paooKX-Hq7LvyyfIbwNsVVU',
    'X-Goog-FieldMask': 'places.displayName,places.primaryType,places.types'
}
        geoReq = requests.get(url, headers=headers, json=data)
        if geoReq.status_code == 200:
            return jsonify(geoReq.json()), 200

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#getting the walkability score of the given latitude and longitude
@app.route('/api/v1/walkability/<lat>/<lng>/<fullAddress>', methods=['GET'])
def walkability(lat,lng, fullAddress):
    try:
        api_key="5e775c237088586a07f1a8ba73969b1a"
        url = f"https://api.walkscore.com/score?format=json&address={fullAddress}&lat={lat}&lon={lng}&wsapikey={api_key}"
        response = requests.get(url)
        return response.json()

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#predicting the price of the house
@app.route('/api/v1/predict-price', methods=['POST'])
def predict_price():
    try:
        df=pd.DataFrame(request.json)
        numerical_data = numerical_transformer.transform(df[numerical_features])
        categorical_data = categorical_transformer.transform(df[categorical_features]).toarray()
        features = np.concatenate([numerical_data, categorical_data], axis=1)

        predicted_price = model.predict(features)
        return predicted_price[0][0]

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500

if __name__ == '__main__':
    try:
        app.logger.info("Starting the server...")
        serve(app, host="localhost", port=8080)
    except Exception as e:
        app.logger.error(f"Failed to start the server: {e}")
