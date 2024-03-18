import json
from urllib import request
import requests

def bhashini_translator(item, lang):
    try:
     
        values_to_translate = []
        
        # Extract values to translate
        values_to_translate.append(item["item_details"]["descriptor"]["name"])
        values_to_translate.append(item["item_details"]["descriptor"]["short_desc"])
        values_to_translate.append(item["item_details"]["descriptor"]["long_desc"])
        values_to_translate.append(item["item_details"]["quantity"]["unitized"]["measure"]["unit"])
        values_to_translate.append(item["item_details"]["price"]["value"])

        # Optionally append values if they exist
        if "@ondc/org/statutory_reqs_packaged_commodities" in item.get("item_details", {}):
            statutory_details = item["item_details"]["@ondc/org/statutory_reqs_packaged_commodities"]
            values_to_translate.append(statutory_details.get("manufacturer_or_packer_name", None))
            values_to_translate.append(statutory_details.get("manufacturer_or_packer_address", None))
            values_to_translate.append(statutory_details.get("common_or_generic_name_of_commodity", None))

        values_to_translate.append(item["providers"][0]["descriptor"]["name"])
        values_to_translate.append(item["providers"][0]["descriptor"]["short_desc"])
        values_to_translate.append(item["providers"][0]["descriptor"]["long_desc"])
        
        # Prepare data for translation
        json_data = json.dumps(values_to_translate)
        print("Data to translate:", json_data)
        
   
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
                        "source": json_data
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
        translated_values = response.json()["pipelineResponse"][0]["output"][0]["target"].replace("\\", "").split(",")
        translated_values = [value.strip()[1:-1] for value in translated_values]

        print("Translation result:", translated_values)
        item["item_details"]["descriptor"]["name"]=translated_values[0]
        item["item_details"]["descriptor"]["short_desc"]=translated_values[1]
        item["item_details"]["descriptor"]["long_desc"]=translated_values[2]
        item["item_details"]["quantity"]["unitized"]["measure"]["unit"]=translated_values[3]
        item["item_details"]["price"]["value"]=translated_values[4]

        if "@ondc/org/statutory_reqs_packaged_commodities" in item.get("item_details", {}):
            statutory_details = item["item_details"]["@ondc/org/statutory_reqs_packaged_commodities"]
            item["item_details"]["@ondc/org/statutory_reqs_packaged_commodities"]["manufacturer_or_packer_name"]=translated_values[5]
            item["item_details"]["@ondc/org/statutory_reqs_packaged_commodities"]["manufacturer_or_packer_address"]=translated_values[6]
            item["item_details"]["@ondc/org/statutory_reqs_packaged_commodities"]["common_or_generic_name_of_commodity"]=translated_values[7]

        if "@ondc/org/statutory_reqs_packaged_commodities" in item.get("item_details", {}):

         item["providers"][0]["descriptor"]["name"]=translated_values[8]
         item["providers"][0]["descriptor"]["short_desc"]=translated_values[9]
         item["providers"][0]["descriptor"]["long_desc"]=translated_values[10]
        else:
         
         item["providers"][0]["descriptor"]["name"]=translated_values[5]
         item["providers"][0]["descriptor"]["short_desc"]=translated_values[6]
         item["providers"][0]["descriptor"]["long_desc"]=translated_values[7] 
        return item 
    except Exception as error:
        print(f"Error: {error}", flush=True)

        return None
