from pydantic import BaseModel

class Worker(BaseModel):
    name: str
    workerID: int