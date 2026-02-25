

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
                     v.uuid as uuid, 
                     b.brand_name as brand_name, 
                     v.complement as complement, 
                     v.year as year, 
                     v.color as color, 
                     v.plate as plate,
                     v.price as price, 
                     v.date_created as date_created
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