from pydantic import BaseModel

class Job(BaseModel):
    name: str
    description: str
    salary_min: float # decimal(8,2)
    salary_max: float # decimal(8,2)

