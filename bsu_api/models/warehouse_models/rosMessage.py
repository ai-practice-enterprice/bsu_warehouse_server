from pydantic import BaseModel

class RosMessage(BaseModel):
    namespace: str
    msg: str
    topic: str

