import unittest
from unittest.mock import MagicMock
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.UpdateVehiclePatch import UpdateVehiclePatch
from app.models.InsertVehicle import InsertVehicle
from app.repositories.VehiclesRepository import VehiclesRepository
from app.services.VehiclesService import VehiclesService
from app import Logger
from app.models.Vehicle import Vehicle

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


    def testGetVehiclesByUUID(self):
        fakeVehicle = {"id": 1, "brand_id": 1, "complement": "Corolla XEi 2.0 Flex 16V Aut. 2020", "year": 2020, "color": "Prata", "price": 15000000, "plate": "ABC1234"}
        self.mockRepo.getVehicleByUUID.return_value = fakeVehicle

        result = self.service.getVehicleByUUID("123e4567-e89b-12d3-a456-426614174000")

        self.assertIsNotNone(result)
        self.assertEqual(result["plate"], "ABC1234")
        self.mockRepo.getVehicleByUUID.assert_called_once_with("123e4567-e89b-12d3-a456-426614174000")

    def testGetVehiclesByPrice(self):
        fakeVehicles = [
            {"id": 1, "brand_id": 1, "complement": "Corolla XEi 2.0 Flex 16V Aut. 2020", "year": 2020, "color": "Prata", "price": 15000000, "plate": "ABC1234"},
            {"id": 2, "brand_id": 2, "complement": "F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021", "year": 2021, "color": "Preta", "price": 30000000, "plate": "XYZ5678"}
        ]
        self.mockRepo.getVehiclesByPrice.return_value = fakeVehicles

        result = self.service.getVehicleByPrice(15000000, 40000000)

        self.assertEqual(len(result), 2)
        self.mockRepo.getVehiclesByPrice.assert_called_once_with(15000000, 40000000, 0, 20)


    def testGetVehicleByYearBrandColorService(self):
        fakeVehicles = [
            {"uuid": 1, "brand_name": "Toyota", "complement": "Corolla XEi 2.0 Flex 16V Aut. 2020", "year": 2020, "color": "Prata", "price": 15000000, "plate": "ABC1234"},
            {"uuid": 2, "brand_name": "Toyota", "complement": "F-150 Lariat 3.5 V6 EcoBoost 4x4 Aut. 2021", "year": 2021, "color": "Preta", "price": 30000000, "plate": "XYZ5678"}
        ]
        self.mockRepo.getVehiclesByBrandYearColor.return_value = fakeVehicles

        result = self.service.getVehiclesByBrandYearColor(2020, "Toyota", "Prata",0,20)

        self.assertEqual(len(result), 2)
        self.mockRepo.getVehiclesByBrandYearColor.assert_called_once_with(2020, "Toyota", "Prata", 0, 20)
    
    def testGetVehicleReportByBrand(self):
        fakeReport = [
            {"brand_name": "Toyota", "total_vehicles": 10},
            {"brand_name": "Ford", "total_vehicles": 5}
        ]
        self.mockRepo.getVehicleReportByBrand.return_value = fakeReport

        result = self.service.getVehicleReportByBrand()

        self.assertEqual(len(result), 2)
        self.mockRepo.getVehicleReportByBrand.assert_called_once()

    def testUpdateCompleteVehicle(self):
        fakeVehicle = {"id": 1, "brand_id": 1, "complement": "Corolla XEi 2.0 Flex 16V Aut. 2020", "year": 2020, "color": "Prata", "price": 15000000, "plate": "ABC1234"}
        self.mockRepo.getVehicleByUUID.return_value = fakeVehicle

        updatedVehicle = InsertVehicle(
            brand_id=1,
            complement="novo complement",
            year=2020,
            color="Prata",
            price=15000000,
            plate="NEWPLATE"
        )
        self.mockRepo.updateCompleteVehicle.return_value = True

        result = self.service.updateCompleteVehicle("123e4567-e89b-12d3-a456-426614174000", updatedVehicle)

        self.assertTrue(result)
        self.mockRepo.updateCompleteVehicle.assert_called_once_with("123e4567-e89b-12d3-a456-426614174000", updatedVehicle)

    def testDeleteVehicle(self):
        self.mockRepo.deleteVehicle.return_value = True

        result = self.service.deleteVehicle("123e4567-e89b-12d3-a456-426614174000")
        self.assertTrue(result)
        self.mockRepo.deleteVehicle.assert_called_once_with("123e4567-e89b-12d3-a456-426614174000", False)

    def testUpdatePatchVehicle(self):
        fakeVehicle = {"id": 1, "brand_id": 1, "complement": "Corolla XEi 2.0 Flex 16V Aut. 2020", "year": 2020, "color": "Prata", "price": 15000000, "plate": "ABC1234"}
        self.mockRepo.getVehicleByUUID.return_value = fakeVehicle

        updatedData = UpdateVehiclePatch(
            complement="novo complement",
            price=20000000
        )
        self.mockRepo.updatePatchVehicle.return_value = True

        result = self.service.updatePatchVehicle("123e4567-e89b-12d3-a456-426614174000", updatedData)

        self.assertTrue(result)
        self.mockRepo.updatePatchVehicle.assert_called_once_with("123e4567-e89b-12d3-a456-426614174000", updatedData)