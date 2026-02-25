from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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
    
    # if  any([ano, marca, cor ]) and not any([minPreco, maxPreco]):
    #     logger.info(f"getting vehicles with filters: ano={ano}, marca={marca}, cor={cor}")


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

# @router.get("/veiculos?minPreco={minPrice}&maxPreco={maxPrice}")
# def getVehicleByPrice(minPrice: int, maxPrice: int, data: dict = Depends(getAuthData), db: Session = Depends(getDB)):
#     logger.info(f"Attempting to retrieve vehicles with price between {minPrice} and {maxPrice} for user: {data['user']}")
#     if not int(minPrice) >= 0 or not int(maxPrice) >= 0:
#         logger.warning(f"Invalid price range: minPrice={minPrice}, maxPrice={maxPrice}")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Price values must be non-negative integers!"
#         )
    
#     if minPrice > maxPrice:
#         logger.warning(f"Invalid price range: minPrice={minPrice} is greater than maxPrice={maxPrice}")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="minPrice cannot be greater than maxPrice!"
#         )
    
#     minPrice = int(minPrice)*100
#     maxPrice = int(maxPrice)*100

#     repository = VehiclesRepository(db)
#     service = VehiclesService(repository)
#     vehicles: list[Vehicle] | None = service.getVehicleByPrice(minPrice, maxPrice)

#     return {"vehicles": vehicles}