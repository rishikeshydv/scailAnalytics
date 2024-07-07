from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
#Load Environment Variables
PRICE_TREND_GPT_API_KEY = os.getenv("PRICE_TREND_GPT_API_KEY")
SCAIL_CONTACT_BOT_API_KEY=os.getenv("SCAIL_CONTACT_BOT_API_KEY")
PRICE_TREND_GPT_MODEL = os.getenv("PRICE_TREND_GPT_MODEL")
SCAIL_CONTACT_BOT_MODEL = os.getenv("SCAIL_CONTACT_BOT_MODEL")
class Finetune:
    def __init__(self):
        #self.secretKey=SCAIL_CONTACT_BOT_API_KEY  #for price trend analyzer
        self.secretKey=PRICE_TREND_GPT_API_KEY  #for scail contact bot
        self.client = OpenAI(api_key=self.secretKey)    

#this finetunes the price-trend analyzer bot
    def finetunePriceTrend(self):
        trainingFile = self.client.files.create(
            file=open("backend/src/price_trend_bot/trainingFiles/training_price_trend.jsonl","rb"),
                    purpose="fine-tune")
        
        validationFile = self.client.files.create(
            file=open("backend/src/price_trend_bot/validationFiless/validation_price_trend.jsonl","rb"),
                    purpose="fine-tune")
        
        print("Training File ID: ",trainingFile.id)
        print("Validation File ID: ",validationFile.id)

        finetuneRes = self.client.fine_tuning.jobs.create(
            training_file=trainingFile.id,
            validation_file=validationFile.id,
            model=PRICE_TREND_GPT_MODEL,
        )
        print(finetuneRes)
        return "Model Finetuned"

#this finetunes the scail contact bot
    def finetuneScailAI(self):
        trainingFile = self.client.files.create(
            file=open("backend/src/price_trend_bot/trainingFiles/training_scail_ai.jsonl","rb"),
                    purpose="fine-tune")
        
        validationFile = self.client.files.create(
            file=open("backend/src/price_trend_bot/validationFiles/validation_scail_ai.jsonl","rb"),
                    purpose="fine-tune")
        
        print("Training File ID: ",trainingFile.id)
        print("Validation File ID: ",validationFile.id)

        finetuneRes = self.client.fine_tuning.jobs.create(
            training_file=trainingFile.id,
            validation_file=validationFile.id,
            model=SCAIL_CONTACT_BOT_MODEL,
        )
        print(finetuneRes)
        return "Model Finetuned"

#finetuneInstance = Finetune()
#finetuneInstance.finetunePriceTrend()
#finetuneInstance.finetuneScailAI()