import unittest
from unittest.mock import MagicMock
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.repositories.VehiclesRepository import VehiclesRepository
from app.services.VehiclesService import VehiclesService
from app import Logger

logger = Logger.createLogger(__name__)

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestsVehicleService(unittest.TestCase):
    def setUp(self):
        self.mockRepo = MagicMock(spec=VehiclesRepository)
        self.service = VehiclesService(self.mockRepo)


    def testGetAllVehicles(self):
        fakeVehicles = [
            {"id": 1, "brand_id": 1, "complement": "Corolla XEi 2.0 Flex 16V Aut. 2020", "year": 2020, "color": "Prata", "price": 15000000, "plate": "ABC1234"},
            {"id": 2, "brand_id": 2, "complement": "F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021", "year": 2021, "color": "Preta", "price": 30000000, "plate": "XYZ5678"},
            {"id": 3, "brand_id": 3, "complement": "Silverado LTZ 5.3 V8 FlexPower Aut. 2018", "year": 2018, "color": "Branca", "price": 25000000, "plate": "DEF9876"}
        ]
        self.mockRepo.getAllVehicles.return_value = fakeVehicles

        result = self.service.getAllVehicles()

        self.assertEqual(len(result), 3)
        self.mockRepo.getAllVehicles.assert_called_once()