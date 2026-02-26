from typing import Optional
from pydantic import BaseModel

class UpdateVehiclePatch(BaseModel):
    brand_id: Optional[int] = None
    complement: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    price: Optional[float] = None
    plate: Optional[str] = None