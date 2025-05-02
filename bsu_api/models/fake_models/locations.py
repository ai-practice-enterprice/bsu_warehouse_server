from pydantic import BaseModel

class Location(BaseModel):
    name: str
    location_type: str # enum = {"pickup point","distribution center","airport"}
    contact_number: str
    opening_hours: str

