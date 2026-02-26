
import os
import time
import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.InsertVehicle import InsertVehicle
from app.repositories.VehiclesRepository import VehiclesRepository
from app import Logger
from app.models.Vehicle import Vehicle
from pathlib import Path

logger = Logger.createLogger(__name__)

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

current_file = Path(__file__).resolve()
root_dir = current_file.parents[2]
sqlPathVehicles = root_dir / "init-scripts" / "2createVehiclesTable.sql"

class TestsVehicleRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(sqlPathVehicles, "r") as f:
            sql_script = f.read()

        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(sql_script))
        logger.info(f"Database schema synchronized from SQL file. {sqlPathVehicles}")

    def setUp(self):
        self.dbSession = TestingSessionLocal()
        self.dbSession.execute(text("TRUNCATE TABLE vehicles RESTART IDENTITY CASCADE"))
        self.dbSession.execute(text("TRUNCATE TABLE brands RESTART IDENTITY CASCADE"))
        self.dbSession.commit()
        # time.sleep(1)

    def tearDown(self):
        self.dbSession.close()

    def testFilePath(self):
        logger.info(f"Database schema synchronized from SQL file. {sqlPathVehicles}")
        self.assertTrue(os.path.isfile(sqlPathVehicles), f"SQL file not found at path: {sqlPathVehicles}")

    def testGetAllVehiclesEmpty(self):
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle]  = repo.getAllVehicles()
        self.assertEqual(len(vehicles), 0)


    def testGetAllVehiclesWithContent(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (brand_id, complement, year, color, price, plate) values
        (1, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234'),
        (2, 'F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021', 2021, 'Preta', 30000000, 'XYZ5678'),
        (3, 'Silverado LTZ 5.3 V8 FlexPower Aut. 2018', 2018, 'Branca', 25000000, 'DEF9876')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle] = repo.getAllVehicles()
        self.assertEqual(len(vehicles), 3)

    def testGetVehiclesByUUID(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (uuid, brand_id, complement, year, color, price, plate) values
        ('123e4567-e89b-12d3-a456-426614174000', 1, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicle: Vehicle = repo.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.plate, "ABC1234")

    def testGetVehiclesByPriceRange(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (brand_id, complement, year, color, price, plate) values
        (1, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234'),
        (2, 'F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021', 2021, 'Preta', 30000000, 'XYZ5678'),
        (3, 'Silverado LTZ 5.3 V8 FlexPower Aut. 2018', 2018, 'Branca', 25000000, 'DEF9876')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle] = repo.getVehiclesByPrice(20000000, 35000000)
        self.assertEqual(len(vehicles), 2)


    def testGetVehicleByYearBrandColorRepo(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (brand_id, complement, year, color, price, plate) values
        (1, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234'),
        (2, 'F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021', 2021, 'Preta', 30000000, 'XYZ5678'),
        (3, 'Silverado LTZ 5.3 V8 FlexPower Aut. 2018', 2018, 'Branca', 25000000, 'DEF9876')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle] = repo.getVehiclesByBrandYearColor(brand="Toyota", year=2020, color="Prata")
        self.assertEqual(len(vehicles), 1)
        self.assertEqual(vehicles[0].plate, "ABC1234")

    def testGetReportWithNoVehicles(self):
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle] = repo.getAllVehicles()
        self.assertEqual(len(vehicles), 0)


    def testGetReportVeHiclesWithVehicles(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (brand_id, complement, year, color, price, plate) values
        (1, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234'),
        (2, 'F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021', 2021, 'Preta', 30000000, 'XYZ5678'),
        (3, 'Silverado LTZ 5.3 V8 FlexPower Aut. 2018', 2018, 'Branca', 25000000, 'DEF9876'),
        (3, 'Onix FlexPower Aut. 2025', 2025, 'Branca', 125000000, 'DEF9877'),
        (3, 'Onix FlexPower Aut. 2021', 2021, 'Branca', 125000000, 'DEF9878')
                                    
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle] = repo.getVehicleReportByBrand()
        self.assertEqual(len(vehicles), 3)

    def testUpdateCompleteVehicle(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (uuid, brand_id, complement, year, color, price, plate) values
        ('123e4567-e89b-12d3-a456-426614174000', 2, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicle: Vehicle = repo.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.plate, "ABC1234")
        updatedVehicle = InsertVehicle(
            brand_id=1,
            complement="novo complement",
            year=vehicle.year,
            color=vehicle.color,
            price=vehicle.price_dolar_cents,
            plate="NEWPLATE"
        )

        repo.updateCompleteVehicle("123e4567-e89b-12d3-a456-426614174000", updatedVehicle)
        newData: Vehicle = repo.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(newData.complement, "novo complement")
        self.assertEqual(newData.brand_name, "Toyota")
        self.assertEqual(newData.plate, "NEWPLATE")


    def testDeleteVehicleSoftDelete(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (uuid, brand_id, complement, year, color, price, plate) values
        ('123e4567-e89b-12d3-a456-426614174000', 2, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicle: Vehicle = repo.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")
        self.assertIsNotNone(vehicle)
        repo.deleteVehicle("123e4567-e89b-12d3-a456-426614174000")
        deletedVehicle: Vehicle = repo.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")
        self.assertIsNone(deletedVehicle)
    
    def testDeleteVehicleHardDelete(self):
        self.dbSession.execute(text("""INSERT INTO brands (brand_name) VALUES ('Toyota'),('Ford'),('Chevrolet')"""))
        self.dbSession.execute(text("""INSERT INTO vehicles (uuid, brand_id, complement, year, color, price, plate) values
        ('123e4567-e89b-12d3-a456-426614174000', 2, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicle: Vehicle = repo.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")
        self.assertIsNotNone(vehicle)
        repo.deleteVehicle("123e4567-e89b-12d3-a456-426614174000", hardDelete=True)
        deletedVehicle: Vehicle = repo.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")
        self.assertIsNone(deletedVehicle)
