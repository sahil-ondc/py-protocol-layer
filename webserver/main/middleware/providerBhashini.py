import json
from urllib import request
import requests

def provider_bhashini_translator(item, lang):
    print("Inside provider bhashini translator>>>>", flush=True)
    try:
        print("Data received:", item, flush=True)  # Print the received dictionary
        
        values_to_translate=item["descriptor"]["name"]
        print("Values to translate:", values_to_translate, flush=True)

        data = {
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": "en",
                            "targetLanguage": f"{lang}"
                        },
                        "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                    }
                }
            ],
            "inputData": {
                "input": [
                    {
                        "source": values_to_translate
                    }
                ]
            }
        }

        # Send translation request
        config = {
            "headers": {
                "Authorization": "5bcJyckKIeDJXW9x_C9gs7P7Rt1goop7SmPyrrdKHF5_4XrWrtMCJaVL8RO8hEJ8",  # Replace with your actual authorization token
                "Content-Type": "application/json"
            },
            "data": json.dumps(data)
        }
        response = requests.post("https://dhruva-api.bhashini.gov.in/services/inference/pipeline", **config)

        # Extract translated data
        translated_values = response.json()["pipelineResponse"][0]["output"][0]["target"]
        print("Translated values:", translated_values, flush=True)
        item["descriptor"]["name"] = translated_values

        return item
        # Rest of your code here
        # ...
    except Exception as error:
        print("Error:", error)
        return None
