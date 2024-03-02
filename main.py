import requests
from datetime import *
import time
import os
#


APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

exercise_endpoint ="https://trackapi.nutritionix.com/v2/natural/exercise"

query_input = input("What exercise have you done? ")

parameters_for_exercise = {
    "query": query_input,
    "gender": "male",
    "weight_kg": 80,
    "height_cm": 193.64,
    "age": 19
}
date = date.today().strftime("%d/%m/%Y")

response = requests.post(url=exercise_endpoint, json=parameters_for_exercise, headers=headers)

# Filling in of the google sheet
sheets_endpoint = os.environ["SHEET_ENDPOINT"]
token = os.environ["TOKEN"]

file = response.json()
print(file)
currentTime = datetime.now().strftime("%H:%M:%S")
exercise = file["exercises"][0]["name"]
duration = file["exercises"][0]["duration_min"]
calories = file["exercises"][0]["nf_calories"]

newData = {
    "workout": {
        "date": date,
        "time": currentTime,
        "exercise": exercise.title(),
        "duration": duration,
        "calories": calories,
    }
}
print(token)
sheetyHeaders = {
    "Authorization": f"Bearer {token}",
}


sheets = requests.post(url=sheets_endpoint,json=newData, headers=sheetyHeaders)
sheets.raise_for_status()