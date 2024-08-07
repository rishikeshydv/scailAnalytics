import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
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
        #show the information in the document
        # info = db.collection('User_Info').document('testuser1@gmail.com').get().to_dict()
        # print(info)
