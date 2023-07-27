import requests
from fastapi import FastAPI,Request
from datetime import datetime
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
# from model import User,Data
from app.helper import get_info,get_map


app = FastAPI(title="Flight Tracker Api",description="It is an api which collects information of a flight with their icao code in realtime")
soup = BeautifulSoup()



@app.get('/data/{flight_number}')
def get_img(flight_number:str):

    current_date = datetime.now()

    access_key = ['eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiMDA1YmEwNWEwZjU1ZDY3MzE3MDAwYzlhMTY1ZDBiNTMxNWYyNTdkNWVkZDlmMzJhMjU4MmI5OTA2MmQ0ZjQ3ZTc1Y2E3YWMyZDk4YzQyNDUiLCJpYXQiOjE2OTAxODc4NTEsIm5iZiI6MTY5MDE4Nzg1MSwiZXhwIjoxNzIxODEwMjUxLCJzdWIiOiI3OTY0Iiwic2NvcGVzIjpbXX0.XNsb7vRk48oqiHLH7xCCO7Jd27gNA-YrAmriV4746YEuU51_Ow-jWYX9-eTy_Fma0V8UyEGWSoyGW9eYPwJs7A','eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiMmIyMDIyNjJkZjI0ZGNkNzRkNmVlZjExZmMzYjczM2VkNmMzYWE5NDIyY2ZmOTE2YWIyZWU4OGNlMTAyNzE0NjcxMDA5ODU4NTAzZTViY2EiLCJpYXQiOjE2ODg5MTI4NzMsIm5iZiI6MTY4ODkxMjg3MywiZXhwIjoxNzIwNTM1MjczLCJzdWIiOiIyMTM0NCIsInNjb3BlcyI6W119.L_ud-0RQkmE0tXr5JBrPU5RxYwhHf054lm8EKGwVDBMcC9e12Xs0F8O1w5ohejxNPpTK9CZ5poOJbER0w-U0TQ',]
    key = access_key[0]
    test_url = f'https://app.goflightlabs.com/flights?access_key={key}'
    test_result = requests.get(test_url).json()

    try:
        if(test_result["message"]):
            key = access_key[1]
    except:
        pass

    url2 = f'https://app.goflightlabs.com/flights?access_key={key}&flightIata={flight_number}'
    api_result = requests.get(url2).json()
    
    if(api_result["success"]):
        url1 = f'https://app.goflightlabs.com/flight?access_key={key}&flight_number={flight_number}'
        schedule_result = requests.get(url1).json()
        print(schedule_result)
        for data in schedule_result["data"]:

            if(data["DATE"] == current_date.strftime("%d %b %Y")):
                api_result["data"][0]["schedule"] = data
    
        return {"success": api_result}
    else:
        return {"success":"false"}


@app.get('/map/departure={departure}&arrival={arrival}',response_class=HTMLResponse)
async def maps(departure:str,arrival:str,request:Request):
    get_map(departure,arrival)
    templates = Jinja2Templates(directory='app/html')
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
