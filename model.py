from pydantic.schema import Optional
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password:str

class Arrival(BaseModel):
    arrival_airport: str
    arrival_timezone: str
    arrival_iata: str
    arrival_icao: str
    arrival_terminal: str
    arrival_gate: str
    arrival_baggage: Optional[int]
    arrival_delay: Optional[int]
    arrival_scheduled: str
    arrival_estimated: str
    arrival_actual: str
    arrival_estimated_runway: str
    arrival_actual_runway: str

class Departure(BaseModel):
    departure_airport: str
    departure_timezone: str
    departure_iata: str
    departure_icao: str
    departure_terminal: str
    departure_gate: str
    departure_baggage: Optional[int]
    departure_delay: Optional[int]
    departure_scheduled: str
    departure_estimated: str
    departure_actual: str
    departure_estimated_runway: str
    departure_actual_runway: str

class Airline(BaseModel):
    airline_name: str
    airline_iata: str
    airline_icao: str

class Flight(BaseModel):
    flight_number: str
    flight_iata: str
    flight_icao: str

class Aircraft(BaseModel):
    user_id: int
    flight_date: str
    flight_status: str

class Data(Aircraft,Flight,Arrival,Departure,Airline):
    class Config:
        orm_mode = True