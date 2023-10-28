from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os
import sys
import time
from PIL import Image
import cv2
import asyncio

#Authentication 
def ocr_search(file_name):
    sub_key = "5ce3e85541ab4869b9a8882e9c420167"
    endpoint = "https://jarvisocr.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(sub_key))

    print("====READING FILE====")
    read_image = file_name
    read_response = computervision_client.read(read_image, raw=True)

    if read_response.status_code != 200:
        print(f"Error: {read_response.status_code}")
        print(read_response.text)

    read_response = computervision_client.read(read_image , raw = True)

    read_operating_location = read_response.headers["Operation-Location"]

    operation_id = read_operating_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id= operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    final_string = ""

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                #print(line.text)
                final_string += line.text + " "

    print(final_string)
    print("Done")
    exit()


def main():
    
     cap = cv2.VideoCapture(0)
     time.sleep(2)
     while True:

         ret , frame = cap.read()

         if not ret:
             break

       
         file_name = f"ocr_{int(time.time())}.png"
         
         print(file_name)
         cv2.imwrite(file_name , frame)
         ocr_search(file_name=file_name)
        
            

if __name__ == "__main__":
  main()
