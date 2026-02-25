from pydantic import BaseModel

class Vehicle(BaseModel):
    uuid: str
    brand_name: str
    complement: str
    year: int
    color: str
    plate: str | None
    price: int
    date_created: str
