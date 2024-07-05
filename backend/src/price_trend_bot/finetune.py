from openai import OpenAI

class Finetune:
    def __init__(self):
        #self.secretKey="sk-proj-oOIKmJQ5tAJTL0baRdvyT3BlbkFJkLCVSancI3TNukiWlvKy"  #for price trend analyzer
        self.secretKey="sk-proj-DBaaojqg622ljaXkaxorT3BlbkFJIYLDWazWAYlQr6C1DA6g"  #for scail contact bot
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
            model="ft:gpt-3.5-turbo-0125:personal::9hKhCk83",
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
            model="ft:gpt-3.5-turbo-0125:personal::9hVRYHlV",
        )
        print(finetuneRes)
        return "Model Finetuned"

#finetuneInstance = Finetune()
#finetuneInstance.finetunePriceTrend()
#finetuneInstance.finetuneScailAI()