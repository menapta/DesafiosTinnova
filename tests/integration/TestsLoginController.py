from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app 
from app.DBConn import getDB

client = TestClient(app)

def getDb():
    db = MagicMock()
    yield db

class TestsLoginController: 

    def setUp(self): 
        app.dependency_overrides[getDB] = getDb

    def tearDown(self): 
        app.dependency_overrides.clear()

    @patch("app.repositories.LoginRepository.LoginRepository.getUserByUsername")
    def testSuccessLogin(self, mockGetUser): 
        from app.userDB import userDB
        mockGetUser.return_value = userDB(
            uuid="123", 
            username="admin", 
            typeuser="admin"
        )

        response = client.post(
            "/auth/login",
            json={"username": "admin", "password": "123"}
        )

        assert response.status_code == 200
        assert "token" in response.json()

    @patch("app.repositories.LoginRepository.LoginRepository.getUserByUsername")
    def testUnauthorizedLogin(self, mockGetUser): 
        mockGetUser.return_value = None

        response = client.post(
            "/auth/login",
            json={"username": "errado", "password": "errada"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized !"

    def testLoginMissingPassword(self,): 
        response = client.post(
            "/auth/login",
            json={"username": "admin"}
        )

        assert response.status_code == 400