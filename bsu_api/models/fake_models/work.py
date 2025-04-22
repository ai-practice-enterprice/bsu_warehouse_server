from pydantic import BaseModel

class Work(BaseModel):
    queue: str
    payload: str # longtext

