from pydantic import BaseModel

class City(BaseModel):
    name: str
    postcode: str
    
