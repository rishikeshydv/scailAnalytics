from flask import Flask, jsonify, request
from waitress import serve
from flask_cors import CORS
import logging
import requests
from keras.models import load_model
import pandas as pd
from sklearn.pipeline import Pipeline
from price_trend.price import PriceTrend
from price_trend_bot.bot import PriceBot
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import joblib
from dotenv import load_dotenv
import os

load_dotenv()

# Load the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
WALKABILITY_API_KEY = os.getenv("WALKABILITY_API_KEY")
#firebase config
class FirebaseConfig:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("config.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': DATABASE_URL
            })
        self.db = firestore.client()
    
    def initialize_firebase(self):
        return self.db
    
# Setting up a Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

########################################## HOUSE PRICE PREDICTION MODEL ###############################################
#loading the model
house_prediction_model = load_model('house_price_prediction_model.h5')
preprocessor1 = joblib.load('price_preprocessor.pkl')

numerical_features_1 = ['bed', 'bath', 'acre_lot', 'house_size','zip_code','street']
categorical_features_1 = ['city', 'state']
####################################################################################################################

######################################### HOUSE RENT PREDICTION MODEL #################################
##############
#loading the model
rent_prediction_model = load_model('rent_prediction_model.h5')
preprocessor2 = joblib.load('rent_preprocessor.pkl')

numerical_features_2 = ['bed', 'bath', 'acre_lot', 'house_size','zip_code','street','price']
categorical_features_2 = ['city', 'state']
########################################################################################################
############


########################################## SALES PROBABILITY MODEL ###############################################
#loading the model
sales_prediction_model = load_model('sales_probability_prediction_model.h5')
preprocessor3 = joblib.load('sales_probability_preprocessor.pkl')

numerical_features_3 = ['bed', 'bath', 'acre_lot', 'house_size','zip_code','street','price']
categorical_features_3 = ['city', 'state']
####################################################################################################################

#price trend for individual property
@app.route('/api/v1/price-trend/individual-property', methods=['POST'])
def individual_property_price_trend():
    try:
        propertyInfo = request.json
        res = PriceBot().individual_price_trend(propertyInfo['current_price'], propertyInfo['predicted_price'])
        return jsonify(message=res), 200
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#price trend for a street
@app.route('/api/v1/price-trend/street', methods=['POST'])
def street_price_trend():
    try:
        streetInfo = request.json
        res = PriceTrend().street_property_price_trend(streetInfo['street'], streetInfo['city'], streetInfo['county'] ,streetInfo['state'])
        return jsonify(message=res), 200
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#price trend for a county
@app.route('/api/v1/price-trend/county', methods=['POST'])
def county_price_trend():
    try:
        streetInfo = request.json
        res = PriceTrend().county_property_price_trend(streetInfo['county'], streetInfo['city'] ,streetInfo['state'])
        return jsonify(message=res), 200
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#price trend for a city
@app.route('/api/v1/price-trend/city', methods=['POST'])
def city_price_trend():
    try:
        streetInfo = request.json
        res = PriceTrend().city_property_price_trend( streetInfo['city'],streetInfo['state'])
        return jsonify(message=res), 200
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#price trend for a state
@app.route('/api/v1/price-trend/state', methods=['POST'])
def state_price_trend():
    try:
        streetInfo = request.json
        res = PriceTrend().state_property_price_trend(streetInfo['state'])
        return jsonify(message=res), 200
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#getting the walkability score of the given latitude and longitude
@app.route('/api/v1/walkability', methods=['POST'])
def walkability():
    try:
        reqData = request.json
        fullAddress = reqData['fullAddress']
        lat = reqData['latitude']
        lng = reqData['longitude']
        url = f"https://api.walkscore.com/score?format=json&address={fullAddress}&lat={lat}&lon={lng}&transit=1&bike=1&wsapikey={WALKABILITY_API_KEY}"
        response = requests.get(url)
        return jsonify(walkabilityData=response.json()), 200

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#getting the transit score of the given latitude and longitude
@app.route('/api/v1/transit', methods=['POST'])  
def transit():
    try:
        reqData = request.json
        city = reqData['city']
        state = reqData['state']
        lat = reqData['latitude']
        lng = reqData['longitude']
        url = f"https://transit.walkscore.com/transit/score/?lat={lat}&lon={lng}&city={city}&state={state}&wsapikey={WALKABILITY_API_KEY}"
        returnData = requests.get(url)
        return jsonify(transitData=returnData.json()), 200

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
#predicting the price of the house
@app.route('/api/v1/predict-price', methods=['POST'])
def predict_price():
    try:
        df=pd.DataFrame(request.json)
        pipeline = Pipeline(steps=[('preprocessor', preprocessor1)])
        df_preprocessed = pipeline.transform(df)
        res = house_prediction_model.predict(df_preprocessed)
        predicted_price = int(round(res[0][0]))
        return jsonify(price=predicted_price)

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500

#predicting the rent of the house
@app.route('/api/v1/rent-price', methods=['POST'])
def predict_rent():
    try:
        df=pd.DataFrame(request.json)
        pipeline = Pipeline(steps=[('preprocessor', preprocessor2)])
        df_preprocessed = pipeline.transform(df)
        res = rent_prediction_model.predict(df_preprocessed)
        predicted_rent = int(round(res[0][0]))
        return jsonify(rent=predicted_rent)
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500

@app.route('/api/v1/sales-probability', methods=['POST'])
def predict_sales():
    try:
        df=pd.DataFrame(request.json)
        pipeline = Pipeline(steps=[('preprocessor', preprocessor3)])
        df_preprocessed = pipeline.transform(df)
        res = sales_prediction_model.predict(df_preprocessed)
        predicted_probability = int(round(res[0][0]))
        return jsonify(probability=predicted_probability)

    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
    #checking if a current city has high crime rate
@app.route('/api/v1/crime-rate', methods=['POST'])
def check_crime_rate():
    try:
        city = request.json['city']
        state = request.json['state']
        database = FirebaseConfig().initialize_firebase()
        cityData = database.collection('city_crimes').document("scail").get()._data
        cityDataKeys = list(cityData.keys())
        for i in range(len(cityDataKeys)):
            if city.lower() == (cityData[cityDataKeys[i]]['city']).lower() and state.lower() == (cityData[cityDataKeys[i]]['state']).lower():
                return cityData[cityDataKeys[i]]
            else:
                return "safe"
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500

#returning the demography information of a particular city,state
@app.route('/api/v1/demography', methods=['POST'])
def get_demography():
    try:
        city = request.json['city']
        state = request.json['state']
        database = FirebaseConfig().initialize_firebase()
        demographyData = database.collection('demography').document("scail").get()._data
        demographyDataKeys = list(demographyData.keys())
        for i in range(len(demographyDataKeys)):
            if city.lower() == (demographyData[demographyDataKeys[i]]['city']).lower() and state.lower() == (demographyData[demographyDataKeys[i]]['state']).lower():
                return jsonify(demography=demographyData[demographyDataKeys[i]]),200 
    except Exception as e:
        # Log the error message
        app.logger.error(f"Error: {e}")
        return jsonify(error="Internal Server Error"), 500
    
if __name__ == '__main__':
    try:
        #debug mode
        #app.run(debug=True, host='localhost', port=8080)
        #production mode
         app.logger.info("Starting the server...")
         serve(app, host="0.0.0.0", port=8080)
        
    except Exception as e:
        app.logger.error(f"Failed to start the server: {e}")
