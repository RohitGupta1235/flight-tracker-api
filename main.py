import requests
from fastapi import FastAPI
import json
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import pymysql

app = FastAPI()
soup = BeautifulSoup()

db = pymysql.connect(host="sql6.freemysqlhosting.net",user="sql6510524",passwd="nclN7eLPbL",database="sql6510524")

@app.get('/data/{flight_iata}')
def get_info(flight_iata:str):
    params = {
                  'access_key': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiZDM0NjM3M2QyZDYzNDczNWU3MDk1MTJkYTBjNjg2MDU1YTMwYzVkNmY0NTQzMGMyMWExZjZlYWI4OGI1ODg0OTRiNzQ3YTkyZjViYmQ3YTAiLCJpYXQiOjE2NTcxMTI4NjEsIm5iZiI6MTY1NzExMjg2MSwiZXhwIjoxNjg4NjQ4ODYxLCJzdWIiOiI3OTY0Iiwic2NvcGVzIjpbXX0.n5MglGPm75IDzE447m6wCHnN-Od7fCbQE4e3ffY3NKXVCKEbz9hf6NIGaUjXng49Vu77w6vqdWjnvojSx7Ydlg',
                  'flight_iata': f'{flight_iata}'
    }

    api_result = requests.get('https://app.goflightlabs.com/flights', params)

    api_response = api_result.json()
    return api_response


def live_location(icoa:str):
    URL = f"https://opensky-network.org/api/states/all?icao24={icoa}"
    r = requests.get(URL)
    pass


@app.get('/demo/G8320')
def load_info():
    raw_data = open('G8320.json')
    json_data = json.load(raw_data)
    live_location(json_data[0]['flight']['icao'])
    return json_data

@app.post('/user/{email}/{password}')
def create_user(email:str,password:str):
    cursor = db.cursor()
    sql = f"""INSERT INTO `users` (`user_id`, `email`, `password`) VALUES ('', '{email}', '{password}')"""  
    cursor.execute(sql)
    db.commit()  

origins = ["*"]

app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
