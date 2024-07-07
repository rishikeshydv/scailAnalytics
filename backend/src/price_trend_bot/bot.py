from openai import OpenAI

class PriceBot:
    def __init__(self):
        self.secretKey="sk-proj-oOIKmJQ5tAJTL0baRdvyT3BlbkFJkLCVSancI3TNukiWlvKy"
        self.client = OpenAI(api_key=self.secretKey)
        
    def individual_price_trend(self,price,predictedPrice):
        response = self.client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-0125:personal::9hKhCk83",
                              messages=[
                            {"role": "system", "content": "You are a Real Estate Assistant"},
                            {"role": "user", "content": f"The current market price of a property is {price}. The predicted price of the property by an extremely accurate Scail AI is {predictedPrice}. Please analyze this data and provide me with a price analysis of this property."}
])
        return response.choices[0].message.content
    def street_price_trend(self,priceList,avgPrice, street):
      response = self.client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-0125:personal::9hKhCk83",
                              messages=[
                            {"role": "system", "content": "You are a Real Estate Assistant"},
                            {"role": "user", "content": f"Here is a list of prices {priceList} of the properties on {street}. The mean price of the property on {street} is {avgPrice}. Please analyze this data and provide me with the price trend of the property."}
                                        ]
                            )
      return response.choices[0].message.content
    
    def city_price_trend(self,priceList,avgPrice, city):
        response = self.client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-0125:personal::9hKhCk83",
                              messages=[
                            {"role": "system", "content": "You are a Real Estate Assistant"},
                            {"role": "user", "content": f"Here is a list of prices {priceList} of the properties in {city}. The mean price of the property in {city} is {avgPrice}. Please analyze this data and provide me with the price trend of the property."}
                                        ]
                            )
        return response.choices[0].message.content
    
    def county_price_trend(self,priceList,avgPrice, county):
        response = self.client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-0125:personal::9hKhCk83",
                              messages=[
                            {"role": "system", "content": "You are a Real Estate Assistant"},
                            {"role": "user", "content": f"Here is a list of prices {priceList} of the properties in {county}. The mean price of the property in {county} is {avgPrice}. Please analyze this data and provide me with the price trend of the property."}
                                        ]
                            )
        return response.choices[0].message.content
    
    def state_price_trend(self,priceList,avgPrice, state):
        response = self.client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-0125:personal::9hKhCk83",
                              messages=[
                            {"role": "system", "content": "You are a Real Estate Assistant"},
                            {"role": "user", "content": f"Here is a list of prices {priceList} of the properties in {state}. The mean price of the property in {state} is {avgPrice}. Please analyze this data and provide me with the price trend of the property."}
                                        ]
                            )
        return response.choices[0].message.content