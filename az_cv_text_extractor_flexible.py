import os
import validators
import time
from tqdm import tqdm
import json
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
os.system("cls")
okay_response=["yes","y"]
credential_temp={}

def credentials():
    print("Enter \"API_KEY\" of your Az-ComputerVision Resouce")
    api_key = input("---> ")
    credential_temp["API_KEY"]=api_key
    print("Enter ENDPOINT of your Az-ComputerVision Resource")
    endpoint = input("--->")
    credential_temp["ENDPOINT"]=endpoint
    print("Do you want to save these credentials for next time in a json file?")
    res = input("---> ")
    if res in okay_response:
        with open("credential.json", 'w') as json_file:
            json.dump(credential_temp, json_file, indent=4)
            print(f"Data has been saved to credential.json!")
    else:
        pass


if os.path.isfile("credential.json"):
    print(f"The file \"credential.json\" exists in the current directory.")
else:
    credentials()

credential= json.load(open("credential.json"))
API_KEY=credential["API_KEY"]
ENDPOINT=credential["ENDPOINT"]
cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
print("Is your image a URL? If \"NO\", I assume that your Image is on local storage! (Y/N)")
ress = input("---> ")

if ress in okay_response:
    while True:
        print("Input your URL!")
        user_url = input("---> ")
        if validators.url(user_url):
            print("The URL is valid, continuing")
            response= cv_client.read(url=user_url, language='en', raw=True)
            break
        else:
            print("The is Malformed URL, Please try again.")
else:
    while True:
        print("Give \"ABSOLUTE DIRECTORY PATH\" of the image.")
        path = input("---> ")
        print(f"Is the given Path for image file is correct? - {path}")
        resss = input("---> ")
        if resss in okay_response:
            print("Thank you for the URL!")
            response = cv_client.read_in_stream(open(path, 'rb'), language='en', raw=True) # The "rb" stands for "Read Binary"
            break
        else:
            print("Sure, You may try again!")

operationLocation = response.headers['Operation-Location']
operation_id = operationLocation.split('/')[-1]
for i in tqdm(range(100), desc="Processing"):
    time.sleep(0.1)
result = cv_client.get_read_result(operation_id)

if result.status == OperationStatusCodes.succeeded:
    read_results = result.analyze_result.read_results
    for analyzed_result in read_results:
        for line in analyzed_result.lines:
            print(line.text)


