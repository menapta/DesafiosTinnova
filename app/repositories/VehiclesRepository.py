

from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import Logger
from ..models.Vehicle import Vehicle

logger = Logger.createLogger(__name__)


class VehiclesRepository:
    def __init__(self, dbSession: Session):
        self.db = dbSession

    def getAllVehicles(self, offset: int = 0, limit: int = 20) ->list[Vehicle] | None:
        logger.info("Fetching all vehicles")
        query = text("""
            SELECT 
                     v.uuid AS uuid, 
                     b.brand_name AS brand_name, 
                     v.complement AS complement, 
                     v.year AS year, 
                     v.color AS color, 
                     v.plate AS plate,
                     v.price AS price, 
                     v.date_created AS date_created
            FROM vehicles v
            JOIN brands b ON v.brand_id = b.id
            ORDER BY v.date_created DESC             
            OFFSET :offset
            LIMIT :limit
        """)
        result = self.db.execute(query, {"offset": offset, "limit": limit}).fetchall()
        logger.debug(f"Query executed, number of vehicles fetched: {len(result)}")

        if result is None:
            logger.debug(f"No vehicles found with offset: {offset} and limit: {limit}")
            return None
        logger.debug(f"Processing {len(result)} vehicles from query result")
        vehicles = []
        for cell in result:
            logger.debug(f"Processing vehicle: {cell}")
            vehicle = Vehicle(
                uuid=str(cell[0]),
                brand_name=cell[1],
                complement=cell[2],
                year=cell[3],
                color=cell[4],
                plate=cell[5],
                price=cell[6],
                date_created=str(cell[7])
            )
            vehicles.append(vehicle)

        logger.debug(f"Fetched {len(vehicles)} vehicles")
        return vehicles
    
    def getVehicleByUUID(self, uuid: str) -> Vehicle | None:
        logger.info(f"Fetching vehicle with UUID: {uuid}")
        query = text("""
            SELECT 
                     v.uuid AS uuid, 
                     b.brand_name AS brand_name, 
                     v.complement AS complement, 
                     v.year AS year, 
                     v.color AS color, 
                     v.plate AS plate,
                     v.price AS price, 
                     v.date_created AS date_created
            FROM vehicles v
            JOIN brands b ON v.brand_id = b.id
            WHERE v.uuid = :uuid
        """)
        result = self.db.execute(query, {"uuid": uuid}).fetchone()
        logger.debug(f"Query executed for UUID: {uuid}, result: {result}")

        if result is None:
            logger.debug(f"No vehicle found with UUID: {uuid}")
            return None
        
        vehicle = Vehicle(
            uuid=str(result[0]),
            brand_name=result[1],
            complement=result[2],
            year=result[3],
            color=result[4],
            plate=result[5],
            price=result[6],
            date_created=str(result[7])
        )
        logger.debug(f"Vehicle fetched with UUID: {uuid}, vehicle data: {vehicle}")
        return vehicle

    def getVehiclesByPrice(self, minPrice: int, maxPrice: int, offset: int = 0, limit: int = 20) -> list[Vehicle] | None:
        logger.info(f"Fetching vehicles with price between {minPrice} and {maxPrice}, offset: {offset}, limit: {limit}")
        query = text("""
            SELECT 
                     v.uuid AS uuid, 
                     b.brand_name AS brand_name, 
                     v.complement AS complement, 
                     v.year AS year, 
                     v.color AS color, 
                     v.plate AS plate,
                     v.price AS price, 
                     v.date_created AS date_created
            FROM vehicles v
            JOIN brands b ON v.brand_id = b.id
            WHERE v.price >= :minPrice AND v.price <= :maxPrice
            ORDER BY v.date_created DESC             
            OFFSET :offset
            LIMIT :limit
        """)
        result = self.db.execute(query, {"minPrice": minPrice, "maxPrice": maxPrice, "offset": offset, "limit": limit}).fetchall()
        logger.debug(f"Query executed for price range {minPrice}-{maxPrice}, number of vehicles fetched: {len(result)}")

        if result is None:
            logger.debug(f"No vehicles found with price between {minPrice} and {maxPrice}")
            return None
        
        vehicles = []
        for cell in result:
            logger.debug(f"Processing vehicle: {cell}")
            vehicle = Vehicle(
                uuid=str(cell[0]),
                brand_name=cell[1],
                complement=cell[2],
                year=cell[3],
                color=cell[4],
                plate=cell[5],
                price=cell[6],
                date_created=str(cell[7])
            )
            vehicles.append(vehicle)

        logger.debug(f"Fetched {len(vehicles)} vehicles with price between {minPrice} and {maxPrice}")
        return vehicles