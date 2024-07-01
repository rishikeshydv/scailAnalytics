#Market Trends Analysis: Visualize and analyze property price trends over time.

#database structure for a property
#create a new collection called property_history
#property_history -> property_id -> all information
#make sure the property IDs are same for 'presentListings' and 'propertyHistory'
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from backend.firebase import FirebaseConfig
class PriceTrend():
    def __init__(self):
        self.database = FirebaseConfig().initialize_firebase()

    #returns the list [year, price] for the given property_id after retrieving the data from the database
    def individual_property_price_trend(self, property_id):
        propertyData = self.database.collection('property_history').document(property_id).get().to_dict()
        return propertyData['price']
    
if __name__ == "__main__":
    print(PriceTrend().individual_property_price_trend('uuidv4'))

