from pydantic import BaseModel

class Airline(BaseModel):
    name: str
    IATA_code: str
    contact_number: str
    headquarters_location: str
    

