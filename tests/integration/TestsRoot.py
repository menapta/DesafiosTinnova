from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app 
from app.DBConn import getDB

client = TestClient(app)

def getDBMock():
    db = MagicMock()
    yield db
    
class TestsRoot: 
    def setUp(self):
        app.dependency_overrides[getDB] = getDBMock

    def tearDown(self):
        app.dependency_overrides.clear()

    def testAPIrootEndPoint(self): 
        response = client.get("/") 
        assert response.status_code == 200