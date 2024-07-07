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
    def __init__(self):
        self.database = FirebaseConfig().initialize_firebase()
        self.dbRef = self.database.collection('presentListings')

        #defining data structures to store the properties based on different comparisons
        self.sameStreet = {}
        self.sameCity = {}
        self.sameCounty = {}
        self.sameState = {}

    def compareStreet(self,street,county,city,state):
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if (docData['street'] == street and docData['city'] == city and docData['county'] == county and docData['state'] == state):
                    if key not in list(self.sameStreet.keys()):
                        self.sameStreet[key] = docData
                    else:
                        self.sameStreet[key] = docData

        return self.sameStreet

    def compareCity(self,city,state):
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if (docData['city'] == city and docData['state'] == state):
                    if key not in list(self.sameCity.keys()):
                        self.sameCity[key] = docData
                    else:
                        self.sameCity[key] = docData
        return self.sameCity

    def compareCounty(self,county,city,state):
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if (docData['county'] == county and docData['city'] == city and docData['state'] == state):
                    if key not in list(self.sameCounty.keys()):
                        self.sameCounty[key] = docData
                    else:
                        self.sameCounty[key] = docData

        return self.sameCounty

    def compareState(self,state):
        for doc in self.dbRef.stream():
            docKeys = list(doc.to_dict().keys())
            for key in docKeys:
                docData = doc.to_dict()[key]
                if (docData['state'] == state):
                    if key not in list(self.sameState.keys()):
                        self.sameState[key] = docData
                    else:
                        self.sameState[key] = docData

        return self.sameState

