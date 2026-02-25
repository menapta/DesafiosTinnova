
from pydantic import BaseModel

class BaseVehicle(BaseModel):
    complement: str
    year: int
    color: str
    plate: str 
    price: int
    
