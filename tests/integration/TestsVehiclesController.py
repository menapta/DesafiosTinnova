from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.HeaderSecurity import getAuthData
from app.main import app 
from app.DBConn import getDB
from app.models.Vehicle import Vehicle
from app import Logger

logger = Logger.createLogger(__name__)

client = TestClient(app)

def getDb():
    db = MagicMock()
    yield db


class TestsVehiclesController: 

    def setUp(self): 
        app.dependency_overrides[getDB] = getDb

    def tearDown(self): 
        app.dependency_overrides.clear()

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getAllVehicles")
    def testGetAllVehiclesAsUser(self, mockGetAllVehicles): 
        mockUserData = {"user": "test_user", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData
        
        mockGetAllVehicles.return_value = [
            Vehicle(
                uuid="123", 
                brand_name="Toyota", 
                complement="Corolla", 
                year=2020, 
                color="Red", 
                price=1500000,
                plate="ABC1234",
                date_created="2023-01-01T00:00:00",
            ),
            Vehicle(
                uuid="456", 
                brand_name="Honda", 
                complement="Civic", 
                year=2019, 
                color="Blue", 
                price=2000000,
                plate="XYZ5678",
                date_created="2023-01-01T00:00:01",
            )
        ]

        response = client.get("/veiculos")

        assert response.status_code == 200
        assert len(response.json()["vehicles"]) == 2

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getAllVehicles")
    def testGetAllVehiclesAsAdmin(self, mockGetAllVehicles): 
        mockUserData = {"user": "test_admin", "type": "user"}
        app.dependency_overrides[getAuthData] = lambda: mockUserData
        
        mockGetAllVehicles.return_value = [
            Vehicle(
                uuid="123", 
                brand_name="Toyota", 
                complement="Corolla", 
                year=2020, 
                color="Red", 
                price=1500000,
                plate="ABC1234",
                date_created="2023-01-01T00:00:00",
            ),
            Vehicle(
                uuid="456", 
                brand_name="Honda", 
                complement="Civic", 
                year=2019, 
                color="Blue", 
                price=2000000,
                plate="XYZ5678",
                date_created="2023-01-01T00:00:01",
            )
        ]

        response = client.get("/veiculos")

        assert response.status_code == 200
        assert len(response.json()["vehicles"]) == 2

    @patch("app.repositories.VehiclesRepository.VehiclesRepository.getAllVehicles")
    def testGetAllVehiclesNoUserData(self, mockGetAllVehicles): 
        app.dependency_overrides = {}

        response = client.get("/veiculos")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 401
