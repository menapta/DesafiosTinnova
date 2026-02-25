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

