
import os
import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
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
sql_path = root_dir / "init-scripts" / "2createVehiclesTable.sql"

class TestsVehicleRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(sql_path, "r") as f:
            sql_script = f.read()

        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(sql_script))
        logger.info(f"Database schema synchronized from SQL file. {sql_path}")

    def setUp(self):
        self.dbSession = TestingSessionLocal()
        self.dbSession.execute(text("TRUNCATE TABLE vehicles RESTART IDENTITY CASCADE"))
        self.dbSession.commit()

    def tearDown(self):
        self.dbSession.execute(text("TRUNCATE TABLE vehicles RESTART IDENTITY CASCADE"))
        self.dbSession.close()

    def testFilePath(self):
        logger.info(f"Database schema synchronized from SQL file. {sql_path}")
        self.assertTrue(os.path.isfile(sql_path), f"SQL file not found at path: {sql_path}")

    def testGetAllVehiclesEmpty(self):
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle]  = repo.getAllVehicles()
        self.assertEqual(len(vehicles), 0)


    def testGetAllVehiclesWithContent(self):
        self.dbSession.execute(text("""INSERT INTO vehicles (brand_id, complement, year, color, price, plate) values
        (1, 'Corolla XEi 2.0 Flex 16V Aut. 2020', 2020, 'Prata', 15000000, 'ABC1234'),
        (2, 'F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021', 2021, 'Preta', 30000000, 'XYZ5678'),
        (3, 'Silverado LTZ 5.3 V8 FlexPower Aut. 2018', 2018, 'Branca', 25000000, 'DEF9876')
        """))
        self.dbSession.commit()
        repo = VehiclesRepository(self.dbSession)
        vehicles: list[Vehicle] = repo.getAllVehicles()
        self.assertEqual(len(vehicles), 3)