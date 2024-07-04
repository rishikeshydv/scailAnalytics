#take the property-id as input
#returns properties in the same street, same city, same county, same state very similar to the given property-id
#with each properties, there must be a button in the UI 'Compare' that would compare pop up a comparative chart  or table

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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
    
class PropertyCompare:
    def __init__(self,property_id, street, city, county, state, zip):
        self.property_id = property_id
        self.street = street
        self.city = city
        self.county = county
        self.state = state
        self.zip = zip
        self.fullAddress = self.street + self.city + self.state + self.zip
        self.database = FirebaseConfig().initialize_firebase()
        self.dbRef = self.database.collection('propertyHistory')

        #defining data structures to store the properties based on different comparisons
        self.sameStreet = {}
        self.sameCity = {}
        self.sameCounty = {}
        self.sameState = {}

    def compareStreet(self):
        for doc in self.dbRef.stream():
            if (doc.to_dict()['street'] + doc.to_dict()['city'] + doc.to_dict()['county'] + doc.to_dict()['state'] + doc.to_dict()['zip'] ) == self.fullAddress:
                if doc.to_dict()['property_id'] not in self.sameStreet.keys():
                    self.sameStreet[doc.to_dict()['property_id']] = doc.to_dict()
                else:
                    self.sameStreet[doc.to_dict()['property_id']] = doc.to_dict()

        return self.sameStreet

    def compareCity(self):
        for doc in self.dbRef.stream():
            if (doc.to_dict()['city'] + doc.to_dict()['county'] + doc.to_dict()['state'] + doc.to_dict()['zip'] ) == self.city + self.state + self.zip:
                if doc.to_dict()['property_id'] not in self.sameCity.keys():
                    self.sameCity[doc.to_dict()['property_id']] = doc.to_dict()
                else:
                    self.sameCity[doc.to_dict()['property_id']] = doc.to_dict()

        return self.sameCity

    def compareCounty(self):
        for doc in self.dbRef.stream():
            if (doc.to_dict()['county'] + doc.to_dict()['state'] + doc.to_dict()['zip'] ) == self.county + self.state + self.zip:
                if doc.to_dict()['property_id'] not in self.sameCounty.keys():
                    self.sameCounty[doc.to_dict()['property_id']] = doc.to_dict()
                else:
                    self.sameCounty[doc.to_dict()['property_id']] = doc.to_dict()

        return self.sameCounty

    def compareState(self):
        for doc in self.dbRef.stream():
            if (doc.to_dict()['state'] + doc.to_dict()['zip'] ) == self.state + self.zip:
                if doc.to_dict()['property_id'] not in self.sameState.keys():
                    self.sameState[doc.to_dict()['property_id']] = doc.to_dict()
                else:
                    self.sameState[doc.to_dict()['property_id']] = doc.to_dict()

        return self.sameState

