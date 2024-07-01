#Market Trends Analysis: Visualize and analyze property price trends over time.

#database structure for a property
#create a new collection called property_history
#property_history -> property_id -> all information
#make sure the property IDs are same for 'presentListings' and 'propertyHistory'
from main import FirebaseConfig

class PriceTrend():
    def __init__(self):
        self.db = FirebaseConfig().initialize_firebase()

    #returns the list [year, price] for the given property_id after retrieving the data from the database
    def individual_property_price_trend(self, property_id):
        propertyData = self.db.collection('property_history').document(property_id).get().to_dict()
        return propertyData['price']

