from pydantic import BaseModel
from datetime import datetime

class Employee(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: datetime
    nationality: str
    leave_balance: int
    