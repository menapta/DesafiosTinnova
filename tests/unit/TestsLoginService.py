import unittest
from unittest.mock import MagicMock
from app.services.LoginService import LoginService 
from app.repositories.LoginRepository import LoginRepository
from app.models.userDB import userDB

class TestsLoginService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock(spec=LoginRepository)
        self.service = LoginService(self.mock_repo)

    def testLoginSuccess(self):
        fake_user = userDB(uuid="123", username="admin", usertype="admin")
        self.mock_repo.getUserByUsername.return_value = fake_user

        result = self.service.login("admin", "password123")

        self.assertEqual(result.username, "admin")
        self.mock_repo.getUserByUsername.assert_called_once_with("admin", "password123")

    def testLoginFailedUserNotFound(self):
        self.mock_repo.getUserByUsername.return_value = None

        result = self.service.login("usuario_inexistente", "123")

        self.assertIsNone(result)
        self.mock_repo.getUserByUsername.assert_called_once()

if __name__ == "__main__":
    unittest.main()