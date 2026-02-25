from app.repositories import VehiclesRepository

from ..models.Vehicle import Vehicle
from .. import Logger


logger = Logger.createLogger(__name__)

class VehiclesService:

    repository: VehiclesRepository
    def __init__(self, repository: VehiclesRepository):
        self.repository: VehiclesRepository = repository
    
    def getAllVehicles(self, offset: int = 0, limit: int = 20) -> list[Vehicle] | None:
        logger.debug(f"VehiclesService: Fetching vehicles with offset: {offset} and limit: {limit}")
        return self.repository.getAllVehicles(offset, limit)

    def getVehicleByUUID(self, uuid: str) -> Vehicle | None:
        logger.debug(f"VehiclesService: Fetching vehicle with UUID: {uuid}")
        return self.repository.getVehicleByUUID(uuid)
    
    def getVehicleByPrice(self, minPrice: int, maxPrice: int, offset: int = 0, limit: int = 20) -> list[Vehicle] | None:
        logger.debug(f"VehiclesService: Fetching vehicles with price range: {minPrice} to {maxPrice}")
        return self.repository.getVehiclesByPrice(minPrice, maxPrice, offset, limit)
    
    def getVehiclesByBrandYearColor(self, brand: str | None, year: int | None, color: str | None, offset: int = 0, limit: int = 20) -> list[Vehicle] | None:
        logger.debug(f"VehiclesService: Fetching vehicles with filters - Brand: {brand}, Year: {year}, Color: {color}")
        return self.repository.getVehiclesByBrandYearColor(brand, year, color, offset, limit)

    def getVehicleReportByBrand(self) -> list[dict] | None:
        logger.debug("VehiclesService: Fetching vehicle report by brand")
        return self.repository.getVehicleReportByBrand()