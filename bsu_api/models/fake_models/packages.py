from pydantic import BaseModel

class Package(BaseModel):
    reference: str
    status: str
    dimension: str
    name: str
    lastname: str
    receiverEmail: str
    receiver_phone_number: str