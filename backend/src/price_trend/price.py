#Market Trends Analysis: Visualize and analyze property price trends over time.

#database structure for a property
#create a new collection called property_history
#property_history -> property_id -> all information
#make sure the property IDs are same for 'presentListings' and 'propertyHistory'

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
class FirebaseConfig:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("backend/firebase/config.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://speety-2175-default-rtdb.firebaseio.com'
            })
        self.db = firestore.client()
    
    def initialize_firebase(self):
        return self.db
    
class PriceTrend():
    def __init__(self):
        self.database = FirebaseConfig().initialize_firebase()
        self.cityPrice = {}
        self.countyPrice = {}
        self.statePrice = {}
        self.similarProperties = []

    #returns the list [year, price] for the given property_id after retrieving the data from the database
    def individual_property_price_trend(self, propertyData):
        #now we get the predicted price of the property
        predicted_price = requests.post('http://127.0.0.1/api/v1/predict-price',json=propertyData)
        predicted_rent = requests.post('http://127.0.0.1/api/v1/predict-price',json=propertyData)
        return [predicted_price]
    
    #returns the list [year, price] for the given city after retrieving the data from the database
    def city_property_price_trend(self, city):
        cityData = self.database.collection('propertyHistory')
        for doc in cityData.stream():
            if doc.to_dict()['city'] == city:
                if doc.to_dict()['street'] not in self.cityPrice.keys():
                    self.cityPrice[doc.to_dict()['street']] = doc.to_dict()['price']
                else:
                    self.cityPrice[doc.to_dict()['street']]=doc.to_dict()['price']
        avgPrice = 0
        cumulativeSum = 0
        ct = 0
        #now, we find the average price of the city
        for key in self.cityPrice.keys():
            cumulativeSum += self.cityPrice[key]['predictedPrice']
            ct += 1
        avgPrice = cumulativeSum/ct
        return [self.cityPrice, avgPrice]
    
    #returns the list [year, price] for the given county after retrieving the data from the database
    def county_property_price_trend(self, county):
        countyData = self.database.collection('propertyHistory')
        for doc in countyData.stream():
            if doc.to_dict()['county'] == county:
                if doc.to_dict()['street'] not in self.cityPrice.keys():
                    self.countyPrice[doc.to_dict()['street']] = doc.to_dict()['price']
                else:
                    self.countyPrice[doc.to_dict()['street']]=doc.to_dict()['price']
        #now, we find the average price of the county
        avgPrice = 0
        cumulativeSum = 0
        ct = 0
        for key in self.countyPrice.keys():
            cumulativeSum += self.countyPrice[key]['predictedPrice']
            ct += 1
        avgPrice = cumulativeSum/ct
        return [self.countyPrice, avgPrice]
    
    #returns the list [year, price] for the given state after retrieving the data from the database
    def state_property_price_trend(self, state):
        stateData = self.database.collection('propertyHistory')
        for doc in stateData.stream():
            if doc.to_dict()['state'] == state:
                if doc.to_dict()['street'] not in self.statePrice.keys():
                    self.statePrice[doc.to_dict()['street']] = doc.to_dict()['price']
                else:
                    self.statePrice[doc.to_dict()['street']]=doc.to_dict()['price']
        #now, we find the average price of the state
        avgPrice = 0
        cumulativeSum = 0
        ct = 0
        for key in self.statePrice.keys():
            cumulativeSum += self.statePrice[key]['predictedPrice']
            ct += 1
        avgPrice = cumulativeSum/ct
        return [self.statePrice, avgPrice]
if __name__ == "__main__":
    print(PriceTrend().individual_property_price_trend('uuidv4'))
    print(PriceTrend().city_property_price_trend('testCity'))

