

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.InsertVehicle import InsertVehicle
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
            WHERE v.is_deleted = false
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
              AND v.is_deleted = false
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
            WHERE v.price >= :minPrice 
              AND v.price <= :maxPrice
              AND v.is_deleted = false
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

    def getVehiclesByBrandYearColor(self, brand: str | None, year: int | None, color: str | None, offset: int = 0, limit: int = 20) -> list[Vehicle] | None:
        logger.info(f"Fetching vehicles with filters - Brand: {brand}, Year: {year}, Color: {color}, Offset: {offset}, Limit: {limit}")
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
            WHERE b.brand_name = :brand
              AND v.year = :year
              AND v.color = :color
              AND v.is_deleted = false
            ORDER BY v.date_created DESC             
            OFFSET :offset
            LIMIT :limit
        """)
        result = self.db.execute(query, {"brand": brand, "year": year, "color": color, "offset": offset, "limit": limit}).fetchall()
        logger.debug(f"Query executed with filters - Brand: {brand}, Year: {year}, Color: {color}. Number of vehicles fetched: {len(result)}")

        if result is None:
            logger.debug(f"No vehicles found with filters - Brand: {brand}, Year: {year}, Color: {color}")
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

        logger.debug(f"Fetched {len(vehicles)} vehicles with filters - Brand: {brand}, Year: {year}, Color: {color}")
        return vehicles
    
    def getVehicleReportByBrand(self):
        logger.info("Fetching report by brand")
        query = text("""
            SELECT 
                     b.brand_name AS brand_name, 
                     COUNT(v.id) AS total_vehicles
            FROM vehicles v
            JOIN brands b ON v.brand_id = b.id
            GROUP BY b.brand_name
        """)
        result = self.db.execute(query).fetchall()
        logger.debug(f"Query executed for report by brand, number of brands fetched: {len(result)}")

        if result is None:
            logger.debug("No brands found for report")
            return None
        
        report = []
        for cell in result:
            logger.debug(f"Processing brand report: {cell}")
            report.append({
                "brand_name": cell[0],
                "total_vehicles": cell[1]
            })

        logger.debug(f"Fetched report for {len(report)} brands")
        return report
    

    def createVehicle(self, vehicle: InsertVehicle) -> bool:
        logger.info(f"Inserting new vehicle with UUID: {vehicle.uuid}")
        query = text("""
            INSERT INTO vehicles (brand_id, complement, year, color, price, plate)
            VALUES (:brand_id, :complement, :year, :color, :price, :plate)
        """)
        result = self.db.execute(query, {
            "brand_id": vehicle.brand_id,
            "complement": vehicle.complement,
            "year": vehicle.year,
            "color": vehicle.color,
            "price": vehicle.price,
            "plate": vehicle.plate
        })
        self.db.commit()
        logger.debug(f"Vehicle inserted successfully, rows affected: {result.rowcount}")
        return result.rowcount == 1


    def updateCompleteVehicle(self, uuid: str, vehicleData: InsertVehicle) -> bool:
        logger.info(f"Updating vehicle with UUID: {uuid}")
        query = text("""
            UPDATE vehicles
            SET brand_id = :brand_id,
                complement = :complement,
                year = :year,
                color = :color,
                price = :price,
                plate = :plate
            WHERE uuid = :uuid
              AND is_deleted = false
        """)
        result = self.db.execute(query, {
            "brand_id": vehicleData.brand_id,
            "complement": vehicleData.complement,
            "year": vehicleData.year,
            "color": vehicleData.color,
            "price": vehicleData.price,
            "plate": vehicleData.plate,
            "uuid": uuid
        })
        self.db.commit()
        logger.debug(f"Vehicle with UUID: {uuid} updated successfully, rows affected: {result.rowcount}")
        return result.rowcount == 1
    
    def deleteVehicle(self, uuid: str, hardDelete: bool = False) -> bool:
        logger.info(f"Deleting vehicle with UUID: {uuid}")
        
        if hardDelete:
            query = text("""
                DELETE FROM vehicles
                WHERE uuid = :uuid
            """)
            result = self.db.execute(query, {"uuid": uuid})
            self.db.commit()
            logger.debug(f"Vehicle with UUID: {uuid} hard deleted successfully, rows affected: {result.rowcount}")
            return result.rowcount == 1
        
        query = text("""
            UPDATE vehicles
            SET is_deleted = true
            WHERE uuid = :uuid
              AND is_deleted = false
        """)
        result = self.db.execute(query, {"uuid": uuid})
        self.db.commit()
        logger.debug(f"Vehicle with UUID: {uuid} deleted successfully, rows affected: {result.rowcount}")
        return result.rowcount == 1

    # def setVehicleAsDeleted(self, uuid: str) -> bool:
    #     logger.info(f"Setting vehicle with UUID: {uuid} as deleted")
    #     query = text("""
    #         UPDATE vehicles
    #         SET is_deleted = true
    #         WHERE uuid = :uuid
    #     """)
    #     result = self.db.execute(query, {"uuid": uuid})
    #     self.db.commit()
    #     logger.debug(f"Vehicle with UUID: {uuid} set as deleted, rows affected: {result.rowcount}")
    #     return result.rowcount > 0