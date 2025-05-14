from pydantic import BaseModel
from datetime import datetime

class Payroll(BaseModel):
    base_salary: float # decimal(8,2)
    bonus: float # decimal(8,2)
    taxes: float # decimal(8,2)
    net_salary: float # decimal(8,2)
    payment_date: datetime
    
