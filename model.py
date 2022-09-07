from pydantic.schema import Optional
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password:str

class Arrival(BaseModel):
    arrival_airport: Optional[str]
    arrival_timezone: Optional[str]
    arrival_iata: Optional[str]
    arrival_icao: Optional[str]
    arrival_terminal: Optional[str]
    arrival_gate: Optional[str]
    arrival_baggage: Optional[int]
    arrival_delay: Optional[int]
    arrival_scheduled: Optional[str]
    arrival_estimated: Optional[str]
    arrival_actual: Optional[str]
    arrival_estimated_runway: Optional[str]
    arrival_actual_runway: Optional[str]

class Departure(BaseModel):
    departure_airport: Optional[str]
    departure_timezone: Optional[str]
    departure_iata: Optional[str]
    departure_icao: Optional[str]
    departure_terminal: Optional[str]
    departure_gate: Optional[str]
    departure_baggage: Optional[int]
    departure_delay: Optional[int]
    departure_scheduled: Optional[str]
    departure_estimated: Optional[str]
    departure_actual: Optional[str]
    departure_estimated_runway: Optional[str]
    departure_actual_runway: Optional[str]

class Airline(BaseModel):
    airline_name: Optional[str]
    airline_iata: Optional[str]
    airline_icao: Optional[str]

class Flight(BaseModel):
    flight_number: Optional[str]
    flight_iata: Optional[str]
    flight_icao: Optional[str]

class Aircraft(BaseModel):
    user_id: Optional[int]
    flight_date: Optional[str]
    flight_status: Optional[str]

class Data(Aircraft,Flight,Arrival,Departure,Airline):
    class Config:
        orm_mode = True