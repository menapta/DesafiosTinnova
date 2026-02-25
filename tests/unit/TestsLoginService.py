import unittest
from unittest.mock import MagicMock
from app.services.LoginService import LoginService 
from app.repositories.LoginRepository import LoginRepository
from app.models.UserDB import UserDB

class TestsLoginService(unittest.TestCase):
    def setUp(self):
        self.mockRepo = MagicMock(spec=LoginRepository)
        self.service = LoginService(self.mockRepo)

    def testLoginSuccess(self):
        fake_user = UserDB(uuid="123", username="admin", usertype="admin")
        self.mockRepo.getUserByUsername.return_value = fake_user

        result = self.service.login("admin", "password123")

        self.assertEqual(result.username, "admin")
        self.mockRepo.getUserByUsername.assert_called_once_with("admin", "password123")

    def testLoginFailedUserNotFound(self):
        self.mockRepo.getUserByUsername.return_value = None

        result = self.service.login("usuario_inexistente", "123")

        self.assertIsNone(result)
        self.mockRepo   .getUserByUsername.assert_called_once()

if __name__ == "__main__":
    unittest.main()