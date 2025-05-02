from pydantic import BaseModel

class Zone(BaseModel):
    zoneID: int 
    zoneDescription: str
    zoneStatus: str 
