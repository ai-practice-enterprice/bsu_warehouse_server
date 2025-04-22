from pydantic import BaseModel
from datetime import datetime

class Contract(BaseModel):
    start_date: datetime
    end_date: datetime
    status: str
    

