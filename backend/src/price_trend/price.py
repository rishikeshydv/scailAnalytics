#Market Trends Analysis: Visualize and analyze property price trends over time.

#database structure for a property
#create a new collection called property_history
#property_history -> property_id -> all information
#make sure the property IDs are same for 'presentListings' and 'propertyHistory'

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from price_trend_bot.bot import PriceBot
import requests

from dotenv import load_dotenv
import os

load_dotenv()
# Load the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

class FirebaseConfig:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("backend/firebase/config.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': DATABASE_URL
            })
        self.db = firestore.client()
    
    def initialize_firebase(self):
        return self.db
    
class PriceTrend():
    def __init__(self):
        self.database = FirebaseConfig().initialize_firebase()
        self.dbRef = self.database.collection('presentListings')
        #collecting the actual prices of the properties based on different comparisons
        self.actualStreetPrice = []
        self.actualCityPrice = []
        self.actualCountyPrice = []
        self.actualStatePrice = []
        #collecting the predicted prices of the properties based on different comparisons
        self.predictedStreetPrice = []
        self.predictedCityPrice = []
        self.predictedCountyPrice = []
        self.predictedStatePrice = []
        #defining data structures to store the properties based on different comparisons
        self.sameStreet = {}
        self.sameCity = {}
        self.sameCounty = {}
        self.sameState = {}
        self.volatileProperties = {}
    
    def extract_street_name(self,address):
        parts = address.split(' ', 1)  # Split on the first space
        if len(parts) > 1:
            return parts[1]
        return address


    #street
    def street_property_price_trend(self, street, city, county, state):
        #collecting all the properties on the same street
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if ((self.extract_street_name(docData['address'])).lower() == street.lower() and (docData['city']).lower() == city.lower() and (docData['county']).lower() == county.lower() and (docData['state']).lower() == state.lower()):
                    if key not in list(self.sameStreet.keys()):
                        self.sameStreet[key] = docData
                        self.actualStreetPrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedStreetPrice.append(res.json()['price'])
                        #logic for price volatility
                        if abs(int(docData['price']) - res.json()['price']) > 80000:
                            self.volatileProperties[key] = docData
                    else:
                        self.sameStreet[key] = docData
                        self.actualStreetPrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedStreetPrice.append(res.json()['price'])
                        #logic for price volatility
                        if abs(int(docData['price']) - res.json().price) > 80000:
                            self.volatileProperties[key] = docData
        #now, average prices of the predicted prices
        if (len(self.actualStreetPrice)>0):
            avgPredictedPrice = 0
            cumulativeSum = 0
            ct = 0
            for price in self.predictedStreetPrice:
                cumulativeSum += price
                ct += 1
            avgPredictedPrice = cumulativeSum/ct
            #now, we do the price analysis using price-bot
            resAnalysis = PriceBot().street_price_trend(self.actualStreetPrice, avgPredictedPrice, street)
            #now we return the actual prices, the average predicted price, volatile properties, and all the properties on the same street
            return [self.volatileProperties, self.sameStreet, resAnalysis]
        else:
            return "No properties found on the given street"
    
    #city
    def city_property_price_trend(self,city,state):
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if ((docData['city']).lower() == city.lower() and( docData['state']).lower() == state.lower()):
                    if key not in list(self.sameCity.keys()):
                        self.sameCity[key] = docData
                        self.actualCityPrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedCityPrice.append(res.json()['price'])
                        #logic for price volatility
                        if abs(int(docData['price']) - res.json()['price']) > 80000:
                            self.volatileProperties[key] = docData
                    else:
                        self.sameCity[key] = docData
                        self.actualCityPrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedCityPrice.append(res.json()['price'])
                        #logic for price volatility
                        if abs(int(docData['price']) - res.json()['price']) > 80000:
                            self.volatileProperties[key] = docData
        #now, average prices of the predicted prices
        if (len(self.actualCityPrice)>0): 
            avgPredictedPrice = 0    
            cumulativeSum = 0
            ct = 0
            for price in self.predictedCityPrice:
                cumulativeSum += price
                ct += 1
            avgPredictedPrice = cumulativeSum/ct
            #now, we do the price analysis using price-bot
            resAnalysis = PriceBot().city_price_trend(self.actualCityPrice, avgPredictedPrice, city)
        #now we return the actual prices, the average predicted price, volatile properties, and all the properties in the same city
            return [self.volatileProperties, self.sameCity, resAnalysis]
        else:
            return "No properties found in the given city"
    
    #county
    def county_property_price_trend(self, county,city,state):
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if ((docData['county']).lower() == county.lower() and (docData['city']).lower() == city.lower() and (docData['state']).lower() == state.lower()):
                    if key not in list(self.sameCounty.keys()):
                        self.sameCounty[key] = docData
                        self.actualCountyPrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedCountyPrice.append(res.json()['price'])
                        #logic for price volatility
                        if abs(int(docData['price']) - res.json()['price']) > 80000:
                            self.volatileProperties[key] = docData
                    else:
                        self.sameCounty[key] = docData
                        self.actualCountyPrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedCountyPrice.append(res.json()['price'])
                        #logic for price volatility
                        if abs(int(docData['price']) - res.json().price) > 80000:
                            self.volatileProperties[key] = docData
        #now, average prices of the predicted prices
        if (len(self.actualCountyPrice)>0):
            avgPredictedPrice = 0
            cumulativeSum = 0
            ct = 0
            for price in self.predictedCountyPrice:
                cumulativeSum += price
                ct += 1
            avgPredictedPrice = cumulativeSum/ct
            #now, we do the price analysis using price-bot
            resAnalysis = PriceBot().county_price_trend(self.actualCountyPrice, avgPredictedPrice, county)
            #now we return the actual prices, the average predicted price, volatile properties, and all the properties in the same county
            return [self.volatileProperties, self.sameCounty, resAnalysis]
        else:
            return "No properties found in the given county"
    
    #state
    def state_property_price_trend(self, state):
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if ((docData['state']).lower() == state.lower()):
                    if key not in list(self.sameState.keys()):
                        self.sameState[key] = docData
                        self.actualStatePrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedStatePrice.append(res.json()['price'])
                        #logic for price volatility 
                        if (int(docData['price']) - res.json()['price']) > 80000:
                            self.volatileProperties[key] = docData
                    else:
                        self.sameState[key] = docData
                        self.actualStatePrice.append(int(docData['price']))
                        requestData = {
                            "bed":[int(docData['beds'])],
                            "bath":[int(docData['baths'])],
                            "acre_lot":[float(docData['lotSize'])],
                            "house_size":[int(docData['sqft'])],
                            "zip_code":[int(docData['zip'])],
                            "street":[893593.0],
                            "city":[docData['city']],
                            "state":[docData['state']]
                        }
                        res = requests.post('http://127.0.0.1:8080/api/v1/predict-price',json=requestData)
                        self.predictedStatePrice.append(res.json()['price'])
                        #logic for price volatility
                        if (int(docData['price']) - res.json()['price']) > 80000:
                            self.volatileProperties[key] = docData
        #now, average prices of the predicted prices
        if (len(self.actualStatePrice)>0):
            avgPredictedPrice = 0
            cumulativeSum = 0
            ct = 0
            for price in self.predictedStatePrice:
                cumulativeSum += price
                ct += 1
            avgPredictedPrice = cumulativeSum/ct
            #now, we do the price analysis using price-bot
            resAnalysis = PriceBot().state_price_trend(self.actualStatePrice, avgPredictedPrice, state)
            #now we return the actual prices, the average predicted price, volatile properties, and all the properties in the same state
            return [self.volatileProperties, self.sameState, resAnalysis]
        else:
            return "No properties found in the given state"
if __name__ == "__main__":
    print(PriceTrend().individual_property_price_trend('uuidv4'))
    print(PriceTrend().city_property_price_trend('testCity'))

