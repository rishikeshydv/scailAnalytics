from openai import OpenAI

class PriceBot:
    def __init__(self,priceList,avgPrice):
        self.priceList = priceList
        self.avgPrice = avgPrice
        self.secretKey="sk-proj-oOIKmJQ5tAJTL0baRdvyT3BlbkFJkLCVSancI3TNukiWlvKy"
        self.client = OpenAI(api_key=self.secretKey)
        
    def individual_price_trend(self):
            response = self.client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-0125:personal::9hKhCk83",
                              messages=[
                            {"role": "system", "content": "You are a Real Estate Assistant"},
                            {"role": "user", "content": f"Here is a list of prices of the property/prope
rties {self.priceList}. The mean price of the property is {self.avgPrice}. Please analyze this data and 
provide me with the price trend of the property."}
                                        ]
                            )
            return response.choices[0].message.content