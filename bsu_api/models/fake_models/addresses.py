from pydantic import BaseModel

class Address(BaseModel):
    street: str
    house_number: str


