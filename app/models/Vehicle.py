from app.models.Money import Money

from .BaseVehicle import BaseVehicle

class Vehicle(BaseVehicle):
    uuid: str
    brand_name: str
    date_created: str
    price_in_real: Money | None = None
    price_in_dollar: Money | None = None
    price_dolar_cents: int
