from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.HeaderSecurity import getAuthData
from app.main import app 
from app.DBConn import getDB
from app.models.Vehicle import Vehicle
from app import Logger, PasswordManager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

from app.repositories.VehiclesRepository import VehiclesRepository
from app.services import VehiclesService


logger = Logger.createLogger(__name__)  

client = TestClient(app)

responseVehicles =[
    Vehicle(
        uuid="efcf0467-70df-4cc8-b6b8-682a8b2040ad", 
        brand_name="Toyota", 
        complement="Corolla", 
        year=2020, 
        color="Red", 
        price_dolar_cents=1500000,
        plate="ABC1234",
        date_created="2023-01-01T00:00:00",
    ),
    Vehicle(
        uuid="a123e4567-e89b-12d3-a456-426614174000", 
        brand_name="Honda", 
        complement="Civic", 
        year=2019, 
        color="Blue", 
        price_dolar_cents=2000000,
        plate="XYZ5678",
        date_created="2023-01-01T00:00:01",
    )
]


responseVehiclesToyota =[
    Vehicle(
        uuid="efcf0467-70df-4cc8-b6b8-682a8b2040ad", 
        brand_name="Toyota", 
        complement="Corolla", 
        year=2020, 
        color="Red", 
        price_dolar_cents=1500000,
        plate="ABC1234",
        date_created="2023-01-01T00:00:00",
    ),
    Vehicle(
        uuid="a123e4567-e89b-12d3-a456-426614174000", 
        brand_name="Toyota", 
        complement="Etios", 
        year=2020, 
        color="Red", 
        price_dolar_cents=2000000,
        plate="XYZ5678",
        date_created="2023-01-01T00:00:01",
    )
]

class TestsVehiclesController: 
    def setUp(self):
        self.mockRepo = MagicMock(spec=VehiclesRepository)
        self.service = VehiclesService(self.mockRepo)

    def tearDown(self):
        app.dependency_overrides.clear()

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getAllVehicles")
    def testGetAllVehiclesAsUser(self, mockGetAllVehicles): 
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData
        
        mockGetAllVehicles.return_value = responseVehicles

        response = client.get("/veiculos")

        assert response.status_code == 200
        assert len(response.json()["vehicles"]) == 2

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getAllVehicles")
    def testGetAllVehiclesAsAdmin(self, mockGetAllVehicles): 
        mockUserData = {"user": "test_admin", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData
        
        mockGetAllVehicles.return_value = responseVehicles

        response = client.get("/veiculos")

        assert response.status_code == 200
        assert len(response.json()["vehicles"]) == 2

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getAllVehicles")
    def testGetAllVehiclesNoUserData(self, mockGetAllVehicles): 
        app.dependency_overrides = {}

        response = client.get("/veiculos")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 401


    def testGetVehicleByUUIDNotFound(self):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData

        response = client.get("/veiculos/efcf0467-70df-4cc8-b6b8-682a8b2040ad")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Vehicle not found!"

    def testGetVehicleByUUIDSuccess(self):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData

        with patch("app.repositories.VehiclesRepository.VehiclesRepository.getVehicleByUUID") as mockGetVehicleByUUID:
            mockGetVehicleByUUID.return_value = Vehicle(
                uuid="b17ba30a-8b4f-4e21-9c3a-3e6ad9a096ed", 
                brand_name="Toyota", 
                complement="Corolla", 
                year=2020, 
                color="Red", 
                price_dolar_cents=1500000,
                plate="ABC1234",
                date_created="2023-01-01T00:00:00",
            )

            response = client.get("/veiculos/b17ba30a-8b4f-4e21-9c3a-3e6ad9a096ed")
            logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

            assert response.status_code == 200
            assert response.json()["vehicle"]["uuid"] == "b17ba30a-8b4f-4e21-9c3a-3e6ad9a096ed"


    def testGetVehicleByUUIDNoUserData(self):
        app.dependency_overrides = {}

        response = client.get("/veiculos/efcf0467-70df-4cc8-b6b8-682a8b2040ad")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getVehiclesByPrice")
    def testGetVehiclesByPrice(self, mockGetVehiclesByPrice):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData


        mockGetVehiclesByPrice.return_value = responseVehicles

        response = client.get("/veiculos?minPreco=10000.00&maxPreco=20000")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 200
        assert len(response.json()["vehicles"]) == 2


    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getVehiclesByPrice")
    def testGetVehiclesByWrongPriceNottation(self, mockGetVehiclesByPrice):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData

        response = client.get("/veiculos?minPreco=10000.00&maxPreco=20000.4a4")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 400

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getVehiclesByBrandYearColor")
    def testGetVehiclesByBrandYearColor(self, mockGetVehiclesByBrandYearColor):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData

        mockGetVehiclesByBrandYearColor.return_value = responseVehiclesToyota

        response = client.get("/veiculos?ano=2020&marca=Toyota&cor=Red")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 200
        assert len(response.json()["vehicles"]) == 2


    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getVehicleReportByBrand")
    def testGetVehicleReportByBrand(self, mockGetVehicleReportByBrand):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData

        mockGetVehicleReportByBrand.return_value = [
            {"brand_name": "Toyota", "total_vehicles": 10},
            {"brand_name": "Honda", "total_vehicles": 5}
        ]

        response = client.get("/veiculos/relatorios/por-marca")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 200
        assert len(response.json()["report"]) == 2

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.createVehicle")
    def testCreateVehicleSuccess(self, mockCreateVehicle):
        mockAdminData = {"user": "test_admin", "type": "admin"}
        app.dependency_overrides[getAuthData] = lambda: mockAdminData

        mockCreateVehicle.return_value = True

        response = client.post("/veiculos", json={
            "brand_id": 1,
            "complement": "Corolla",
            "year": 2020,
            "color": "Red",
            "price": 1500000,
            "plate": "ABC2534"
        })
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 200
        assert response.json()["message"] == "Vehicle created successfully!"


    @patch("app.repositories.VehiclesRepository.VehiclesRepository.createVehicle")
    def testCreateVehicleNotAllowed(self, mockCreateVehicle):
        mockAdminData = {"user": "test_admin", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockAdminData

        mockCreateVehicle.return_value = True

        response = client.post("/veiculos", json={
            "brand_id": 1,
            "complement": "Corolla",
            "year": 2020,
            "color": "Red",
            "price": 1500000,
            "plate": "ABC2534"
        })
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 403


    @patch("app.repositories.VehiclesRepository.VehiclesRepository.updateCompleteVehicle")
    def testUpdateCompleteVehicle(self, mockUpdateCompleteVehicle):
        mockAdminData = {"user": "test_admin", "type": "admin"}
        app.dependency_overrides[getAuthData] = lambda: mockAdminData

        mockUpdateCompleteVehicle.return_value = True

        response = client.put("/veiculos/123e4567-e89b-12d3-a456-426614174000", json={
            "brand_id": 1,
            "complement": "Corolla",
            "year": 2020,
            "color": "Red",
            "price": 1500000,
            "plate": "ABC2534"
        })
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 200
        assert response.json()["message"] == "Vehicle updated successfully!"


    @patch("app.repositories.VehiclesRepository.VehiclesRepository.updateCompleteVehicle")
    def testUpdateCompleteVehicleNotAdmin(self, mockUpdateCompleteVehicle):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData

        mockUpdateCompleteVehicle.return_value = True

        response = client.put("/veiculos/123e4567-e89b-12d3-a456-426614174000", json={
            "brand_id": 1,
            "complement": "Corolla",
            "year": 2020,
            "color": "Red",
            "price": 1500000,
            "plate": "ABC2534"
        })
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 403

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.deleteVehicle")
    def testDeleteVehicle(self, mockDeleteVehicle):
        mockAdminData = {"user": "test_admin", "type": "admin"}
        app.dependency_overrides[getAuthData] = lambda: mockAdminData

        mockDeleteVehicle.return_value = True

        response = client.delete("/veiculos/123e4567-e89b-12d3-a456-426614174000")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 200
        assert response.json()["message"] == "Vehicle deleted successfully!"


    @patch("app.repositories.VehiclesRepository.VehiclesRepository.deleteVehicle")
    def testDeleteVehicleNotAllowed(self, mockDeleteVehicle):
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData

        mockDeleteVehicle.return_value = True

        response = client.delete("/veiculos/123e4567-e89b-12d3-a456-426614174000")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 403
