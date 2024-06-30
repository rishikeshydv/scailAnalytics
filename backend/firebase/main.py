import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred,
    {'databaseURL': 'https://speety-2175-default-rtdb.firebaseio.com'}
 )
ref = db.reference('/db_name/collection/docs')
print(ref.get())