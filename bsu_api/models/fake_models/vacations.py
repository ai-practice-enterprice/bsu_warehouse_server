from pydantic import BaseModel
from datetime import datetime

class Vacation(BaseModel):
    vacation_type: str
    start_date: datetime
    end_date: datetime
    approve_status: str # enum('pending','approved','rejected')
    


