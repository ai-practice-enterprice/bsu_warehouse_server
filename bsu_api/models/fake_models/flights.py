from pydantic import BaseModel
from datetime import datetime

class Flight(BaseModel):
    departure_time: datetime
    arrival_time: datetime
    status: str
    