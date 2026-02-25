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