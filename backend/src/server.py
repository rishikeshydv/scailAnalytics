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
from volatility_check.volatile import Volatility
# Setting up a Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Setting up a GPT model API key (placeholder)
apiKey = "your_api_key"

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder()
########################################## HOUSE PREDICTION MODEL ###############################################
#loading the model
house_prediction_model = load_model('backend/src/house_price_prediction_model.keras')

numerical_features = ['bed', 'bath', 'acre_lot', 'house_size','zip_code','street']
categorical_features = ['city', 'state']
####################################################################################################################


########################################## SALES PROBABILITY MODEL ###############################################
#loading the model
sales_prediction_model = load_model('backend/src/sales_probability_prediction_model.keras')

numerical_features = ['bed', 'bath', 'acre_lot', 'house_size','zip_code','street','price']
categorical_features = ['city', 'state']
####################################################################################################################

##############################  CRITERIA FOR PROPERTY IMPROVEMENT AND RENOVATION ################################

renovation_criteria = {
    #bath model
  "bath_model_medium_size": "5 x 7 foot",
  "bath_model_large_size": "9 x 9 foot",

  "bath_model_medium_do_it_yourself": "5000",
  "bath_model_medium_cost_low": "9000",
  "bath_model_medium_cost_high": "14000",

  "bath_model_large_cost_low": "35000",
  "bath_model_large_cost_high": "45000",

  #kitchen model

  "kitchen_model_medium_size": "10 x 10 foot",  # 10x10 is the regular size of a kitchen

  "kitchen_model_medium_do_it_yourself": "10000",

  "bath_model_medium_cost_low": "15000",
  "bath_model_medium_cost_high": "20000",

  "bath_model_high_cost_low": "50000",
  "bath_model_high_cost_high": "65000",

 #roof model

  "roof_model_medium_size": "1700",  # sqft
  "roof_model_large_size": "2100",  # sqft
  "roof_model_do_it_yourself_low": "680",  # asphalt shingles
  "roof_model_do_it_yourself_high": "3700",  # asphalt shingles

  "tile_roof_low": "7650",
  "tile_roof_high": "18000",

  "metal_roof_low": "5100",
  "metal_roof_high": "20000",

  "slate_roof_low": "17000",
  "slate_roof_high": "60000",

  #house clean model

  "house_clean_do_it_yourself_low": "0",

  "house_clean_small_low": "74",  # 900 sqft
  "house_clean_small_high": "200",  # 900 sqft

  "house_clean_medium_low": "95",  # 1300 sqft
  "house_clean_medium_high": "300",  # 1300 sqft

  "house_clean_large_low": "149",  # 2200 sqft
  "house_clean_large_high": "400",  # 2200 sqft

  #central air conditioning model

  "air_conditioning_model_low": "3500",  # 2000 sq ft
  "air_conditioning_model_high": "4000",  # 2000 sq ft

  #water boiler model

  "water_boiler_model_low": "4000",
  "water_boiler_model_high": "28000"
}

 
####################################################################################################################

#price trend for individual property
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

        predicted_price = house_prediction_model.predict(features)
        return predicted_price[0][0]

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500


@app.route('/api/v1/sales-probability', methods=['POST'])
def predict_sales():
    try:
        df=pd.DataFrame(request.json)
        numerical_data = numerical_transformer.transform(df[numerical_features])
        categorical_data = categorical_transformer.transform(df[categorical_features]).toarray()
        features = np.concatenate([numerical_data, categorical_data], axis=1)

        predicted_price = sales_prediction_model.predict(features)
        return predicted_price[0][0]

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500

# financial impact of property improvement and renovations
@app.route('/api/v1/renovation', methods=['GET'])
def renovation():
    return jsonify(renovation_criteria), 200

#checking the volatility of the property
@app.route('/api/v1/volatility', methods=['POST'])
def check_volatility():
    try:
        propertyData =  request.json
        volatile = Volatility(propertyData)
        return volatile.checkVolatility()
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
