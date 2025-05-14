from pydantic import BaseModel
from datetime import datetime

class PackageMovement(BaseModel):
    departure_time: datetime
    arrival_time: datetime
    check_in_time: datetime
    check_out_time: datetime


