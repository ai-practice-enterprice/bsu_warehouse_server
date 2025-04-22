from pydantic import BaseModel

class Airplane(BaseModel):
    model: str
    capacity: int
    status: str
