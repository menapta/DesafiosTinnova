from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.InsertVehicle import InsertVehicle

from ..HeaderSecurity import getAuthData, adminAuthData    
from ..services.VehiclesService import VehiclesService
from ..repositories.VehiclesRepository import VehiclesRepository
from ..DBConn import getDB
from .. import Logger
from ..models.Vehicle import Vehicle
from ..models.VehicleFilters import VehicleFilters

logger = Logger.createLogger(__name__)
router = APIRouter()

@router.get("/veiculos")
def getVehicles(
    filters: VehicleFilters = Depends(),
    offset: int = 0,
    limit: int = 20,
    authData: dict = Depends(getAuthData), 
    db: Session = Depends(getDB)
    ):

    logger.info(f"Attempting to retrieve vehicles for user: {authData['user']}")
    repository = VehiclesRepository(db)
    service = VehiclesService(repository)

    if  any([filters.minPreco, filters.maxPreco]):
        logger.info(f"getting vehicles with price range: minPreco={filters.minPreco}, maxPreco={filters.maxPreco}")

        minPrice = int(filters.minPreco*100)
        maxPrice = int(filters.maxPreco*100)
        vehicles: list[Vehicle] | None = service.getVehicleByPrice(minPrice, maxPrice, offset, limit)
    
    if  any([filters.ano, filters.marca, filters.cor ]): # and not any([filters.minPreco, filters.maxPreco]):
        logger.info(f"getting vehicles with filters: ano={filters.ano}, marca={filters.marca}, cor={filters.cor}")
        vehicles: list[Vehicle] | None = service.getVehiclesByBrandYearColor(
            year=filters.ano,
            brand=filters.marca,
            color=filters.cor,
            offset=offset,
            limit=limit
        )


    if not any([filters.ano, filters.marca, filters.cor, filters.minPreco, filters.maxPreco]):
        logger.info("No filters provided, fetching all vehicles")


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

@router.get("/veiculos/relatorios/por-marca")
def getVehicleReportByBrand(data: dict = Depends(getAuthData), db: Session = Depends(getDB)):
    logger.info(f"Attempting to retrieve vehicle report by brand for user: {data['user']}")
    repository = VehiclesRepository(db)
    service = VehiclesService(repository)
    report = service.getVehicleReportByBrand()
    return {"report": report}

@router.post("/veiculos")
def createVehicle(vehicleData: InsertVehicle, data: dict = Depends(adminAuthData), db: Session = Depends(getDB)):
    logger.info(f"Attempting to create vehicle with data: {vehicleData} for admin user: {data['user']}")
    repository = VehiclesRepository(db)
    service = VehiclesService(repository)
    success = service.createVehicle(vehicleData)

    if not success:
        logger.warning(f"Failed to create vehicle with data: {vehicleData}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create vehicle! {}"
        )
    logger.info(f"Vehicle created successfully with data: {vehicleData}")
    return {"message": "Vehicle created successfully!"}


