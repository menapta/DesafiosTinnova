from fastapi import HTTPException
from app.exceptions.base import EntityNotFoundException, DuplicateEntryException, InvalidYearException
from app.models.InsertVehicle import InsertVehicle
from app.models.UpdateVehiclePatch import UpdateVehiclePatch
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
    
    def getVehiclesByBrandYearColor(self, brand: str | None, year: int | None, color: str | None, 
                                                                offset: int = 0, limit: int = 20) -> list[Vehicle] | None:
        logger.debug(f"VehiclesService: Fetching vehicles with filters - Brand: {brand}, Year: {year}, Color: {color}")
        return self.repository.getVehiclesByBrandYearColor(brand, year, color, offset, limit)

    def getVehicleReportByBrand(self) -> list[dict] | None:
        logger.debug("VehiclesService: Fetching vehicle report by brand")
        return self.repository.getVehicleReportByBrand()

    def createVehicle(self, vehicleData: InsertVehicle) -> bool | None:
        logger.debug(f"VehiclesService: Creating vehicle with data: {vehicleData}")
        try:
            return self.repository.createVehicle(vehicleData)
        except DuplicateEntryException as e:
            raise HTTPException(status_code=409, detail=str(e))
        except InvalidYearException as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def updateCompleteVehicle(self, uuid: str, vehicleData: InsertVehicle) -> bool | None:
        logger.debug(f"VehiclesService: Updating vehicle with UUID: {uuid} using data: {vehicleData}")
        try:
            return self.repository.updateCompleteVehicle(uuid, vehicleData)
        except EntityNotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
        except DuplicateEntryException as e:
            raise HTTPException(status_code=409, detail=e.message) 
        except InvalidYearException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def deleteVehicle(self, uuid: str, hardDelete: bool = False) -> bool | None:
        logger.debug(f"VehiclesService: Deleting vehicle with UUID: {uuid}")
        return self.repository.deleteVehicle(uuid, hardDelete)
    
    def updatePatchVehicle(self, uuid: str, updateData: UpdateVehiclePatch) -> bool | None:
        logger.debug(f"VehiclesService: Partially updating vehicle with UUID: {uuid} using data: {updateData}")
        try:
            return self.repository.updatePatchVehicle(uuid, updateData)
        except EntityNotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
        except DuplicateEntryException as e:
            raise HTTPException(status_code=409, detail=e.message) 
        except InvalidYearException as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")