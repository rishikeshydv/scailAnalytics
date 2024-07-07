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

class Alerts:
    def __init__(self,userState):
        self.user_state = userState
        self.alertProperties = {}

#checking the volatility of all the properties in the state of residence of the user
    def sendAlerts(self):
        #getting the predicted price
        propertyData = self.database.collection('propertyHistory')
        for doc in propertyData.stream():
            if doc.to_dict()['state'] == self.user_state & doc.to_dict()['volatility'] == 'Yes':
                self.alertProperties[doc.to_dict()['property_id']] = doc.to_dict()
        return self.alertProperties