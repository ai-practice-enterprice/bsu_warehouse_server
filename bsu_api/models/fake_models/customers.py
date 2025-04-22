from pydantic import BaseModel

class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str



    
