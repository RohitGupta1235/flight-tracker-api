import requests
from fastapi import FastAPI,Request
import json
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from model import User,Data
from helper import get_info,get_map,get_db


app = FastAPI(title="Flight Tracker Api",description="It is an api which collects information of a flight with their icao code in realtime")
soup = BeautifulSoup()



@app.get('/data/{flight_iata}')
def get_img(flight_iata:str):
    params = {
                  'access_key': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiZDM0NjM3M2QyZDYzNDczNWU3MDk1MTJkYTBjNjg2MDU1YTMwYzVkNmY0NTQzMGMyMWExZjZlYWI4OGI1ODg0OTRiNzQ3YTkyZjViYmQ3YTAiLCJpYXQiOjE2NTcxMTI4NjEsIm5iZiI6MTY1NzExMjg2MSwiZXhwIjoxNjg4NjQ4ODYxLCJzdWIiOiI3OTY0Iiwic2NvcGVzIjpbXX0.n5MglGPm75IDzE447m6wCHnN-Od7fCbQE4e3ffY3NKXVCKEbz9hf6NIGaUjXng49Vu77w6vqdWjnvojSx7Ydlg',
                  'flightIata': f'{flight_iata}'
    }

    api_result = requests.get('https://app.goflightlabs.com/flights', params)

    api_response = api_result.json()
    print(len(api_response[0]))
    if(len(api_response)>3):
        api_response = get_info(api_response)
    return api_response


# def live_location(icoa:str):
#     URL = f"https://opensky-network.org/api/states/all?icao24={icoa}"
#     r = requests.get(URL)
#     pass



# @app.get('/demo/G8320')
# def load_info():
#     raw_data = open('G8320.json')
#     json_data = json.load(raw_data)
#     # live_location(json_data[0]['flight']['icao'])
#     json_data = get_info(json_data)
#     return json_data


@app.get('/map/departure={departure}&arrival={arrival}',response_class=HTMLResponse)
async def maps(departure:str,arrival:str,request:Request):
    get_map(departure,arrival)
    templates = Jinja2Templates(directory='html')
    return templates.TemplateResponse("map.html", {"request": request})

# @app.post('/user')
# def create_user(user:User):
#     db = get_db()
#     cursor = db.cursor()
#     sql = f"""INSERT INTO `User` (`id`, `email`, `password`) VALUES (NULL, '{user.email}', '{user.password}')"""  
#     cursor.execute(sql)
#     id = cursor.lastrowid
#     db.commit()
#     db.close()  
#     return {'id':id}

# @app.post('/data')
# def insert_data(data:Data):
#     db = get_db()
#     # departure_id:int = None
#     # arrival_id:int = None
#     cursor = db.cursor()
#     sql = f"""INSERT INTO `Flight` (`number`, `iata`, `icao`) VALUES ('{data.flight_number}', '{data.flight_iata}', '{data.flight_icao}')"""
#     cursor.execute(sql)
#     print("FLIGHT")
#     sql = f"""INSERT INTO `Departure` (`id`, `airport`, `timezone`, `iata`, `icao`, `terminal`, `gate`, `baggage`, `delay`, `scheduled`, `estimated`, `actual`, `estimated_runway`, `actual_runway`) VALUES (NULL, '{data.departure_airport}', '{data.departure_timezone}', '{data.departure_iata}', '{data.departure_icao}', '{data.departure_terminal}', '{data.departure_gate}', '{data.departure_baggage}', '{data.departure_delay}', '{data.departure_scheduled}', '{data.departure_estimated}', '{data.departure_actual}', '{data.departure_estimated_runway}', '{data.departure_actual_runway}')"""
#     if cursor.execute(sql):
#         departure_id = cursor.lastrowid
#         print("DEPARTURE")
#     sql = f"""INSERT INTO `Arrival` (`id`, `airport`, `timezone`, `iata`, `icao`, `terminal`, `gate`, `baggage`, `delay`, `scheduled`, `estimated`, `actual`, `estimated_runway`, `actual_runway`) VALUES (NULL, '{data.arrival_airport}', '{data.arrival_timezone}', '{data.arrival_iata}', '{data.arrival_icao}', '{data.arrival_terminal}', '{data.arrival_gate}', '{data.arrival_baggage}', '{data.arrival_delay}', '{data.arrival_scheduled}', '{data.arrival_estimated}', '{data.arrival_actual}', '{data.arrival_estimated_runway}', '{data.arrival_actual_runway}')"""
#     if cursor.execute(sql):
#         arrival_id = cursor.lastrowid
#         print("ARRIVAL")
#     sql = f"""INSERT INTO `Airline` (`name`, `iata`, `icao`) VALUES ('{data.airline_name}', '{data.airline_iata}', '{data.arrival_icao}')"""
#     if cursor.execute(sql):
#         print("AIRLINE")
#     sql = f"""INSERT INTO `Aircraft` (`id`, `user_id`, `flight_date`, `flight_status`, `arrival_id`, `departure_id`, `airline_name`, `flight_iata`) VALUES (NULL, '{data.user_id}', '{data.flight_date}', '{data.flight_status}', '{arrival_id}', '{departure_id}', '{data.airline_name}', '{data.flight_iata}')"""
#     if cursor.execute(sql):
#         print("AIRCRAFT")
#     db.commit()
#     db.close()
#     return data

origins = ["*"]

app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
