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

# def getDb():
#     db = MagicMock()
#     yield db

# TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_test"

# engine = create_engine(TEST_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# current_file = Path(__file__).resolve()
# root_dir = current_file.parents[2]
# sqlPathVehicles = root_dir / "init-scripts" / "2createVehiclesTable.sql"

responseVehicles =[
    Vehicle(
        uuid="efcf0467-70df-4cc8-b6b8-682a8b2040ad", 
        brand_name="Toyota", 
        complement="Corolla", 
        year=2020, 
        color="Red", 
        price=1500000,
        plate="ABC1234",
        date_created="2023-01-01T00:00:00",
    ),
    Vehicle(
        uuid="a123e4567-e89b-12d3-a456-426614174000", 
        brand_name="Honda", 
        complement="Civic", 
        year=2019, 
        color="Blue", 
        price=2000000,
        plate="XYZ5678",
        date_created="2023-01-01T00:00:01",
    )
]

class TestsVehiclesController: 
    # @classmethod
    # def setUpClass(cls):
    #     self.mockRepo = MagicMock(spec=VehiclesRepository)
    #     self.service = VehiclesService(self.mockRepo)
        # with open(sqlPathVehicles, "r") as f:
        #     sql_script = f.read()

        # with engine.connect() as conn:
        #     with conn.begin():
        #         conn.execute(text(sql_script))
        # logger.info(f"Database schema synchronized from SQL file. {sqlPathVehicles}")

    def setUp(self):
        self.mockRepo = MagicMock(spec=VehiclesRepository)
        self.service = VehiclesService(self.mockRepo)
        # self.dbSession = TestingSessionLocal()
        # self.dbSession.execute(text("TRUNCATE TABLE vehicles RESTART IDENTITY CASCADE"))
        # self.dbSession.execute(text("TRUNCATE TABLE brands RESTART IDENTITY CASCADE"))
        # self.dbSession.commit()
        # # app.dependency_overrides[getDB] = getDb

    # def tearDown(self): 
    #     self.dbSession.close()
    #     # app.dependency_overrides.clear()
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
                price=1500000,
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

        response = client.get("/veiculos?minPreco=10000.00&maxPreco=20000.4444")
        logger.info(f"Response status code: {response.status_code}, Response body: {response.json()}")

        assert response.status_code == 400
