from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..HeaderSecurity import getAuthData, adminAuthData    
from ..services.VehiclesService import VehiclesService
from ..repositories.VehiclesRepository import VehiclesRepository
from ..DBConn import getDB
from .. import Logger
from ..models.Vehicle import Vehicle

logger = Logger.createLogger(__name__)
router = APIRouter()

@router.get("/veiculos")
def getVehicles(data: dict = Depends(getAuthData), db: Session = Depends(getDB)):
    logger.info(f"Attempting to retrieve vehicles for user: {data['user']}")

    repository = VehiclesRepository(db)
    service = VehiclesService(repository)
    vehicles: list[Vehicle] | None = service.getAllVehicles()

    return {"vehicles": vehicles}

@router.get("/veiculos/{uuid}")
def getVehicleByUUID(uuid: str, data: dict = Depends(getAuthData), db: Session = Depends(getDB)):
    logger.info(f"Attempting to retrieve vehicle with UUID: {uuid} for user: {data['user']}")
    
    repository = VehiclesRepository(db)
    service = VehiclesService(repository)
    vehicle: Vehicle | None = service.getVehicleByUUID(uuid)

    if vehicle is None:
        logger.warning(f"Vehicle with UUID: {uuid} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found!"
        )
    
    return {"vehicle": vehicle}