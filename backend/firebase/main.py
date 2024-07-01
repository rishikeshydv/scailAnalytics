import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirebaseConfig:
    def __init__(self):
        pass
    
    def initialize_firebase(self):
        cred = credentials.Certificate("backend/firebase/config.json")
        firebase_admin.initialize_app(cred,
            {'databaseURL': 'https://speety-2175-default-rtdb.firebaseio.com'}
        )
        db = firestore.client()
        return db
        #show the information in the document
        # info = db.collection('User_Info').document('testuser1@gmail.com').get().to_dict()
        # print(info)


