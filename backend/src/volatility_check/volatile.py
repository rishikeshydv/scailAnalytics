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

class Volatility:
    def __init__(self,property):
        self.property = property
        self.updatedProperty = {}

    def checkVolatility(self):
        #getting the predicted price
        predictedPrice = requests.post("http://http://127.0.0.1:8080/api/v1/predict-price", json=self.property)
        #checking the volatility
        priceDifference = abs(predictedPrice - self.property['price'])
        if priceDifference > 100000:
            self.updatedProperty = self.property
            self.updatedProperty['volatility'] = 'Yes'
        else:
            self.updatedProperty = self.property
            self.updatedProperty['volatility'] = 'No'
        return self.updatedProperty

