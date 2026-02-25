import unittest
from app.PasswordManager import PasswordManager 
from app import Logger

logger = Logger.createLogger(__name__)


class TestsPasswordManager(unittest.TestCase):

    def setUp(self):
        self.pm = PasswordManager()

    def testHashCreation(self):
        password = "minha_senha_secreta"
        hashed = self.pm.hashPassword(password)
        
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(password, hashed)
        self.assertTrue(hashed.startswith('$2b$'))

    def testVerifyCorrectPassword(self):
        password = "12345password"
        hashed = self.pm.hashPassword(password)
        
        result = self.pm.verifyPassword(password, hashed)
        logger.info(f"testVerifyCorrectPassword: {result}")
        print(f"hashed 1: {hashed}")
        print(f"result: {result}")
        self.assertTrue(result)

    def testVerifyWrongPassword(self):
        password = "senha_correta"
        wrongPassword = "senha_errada"
        correctHash = self.pm.hashPassword(password)
        
        result = self.pm.verifyPassword(wrongPassword, correctHash)
        self.assertFalse(result)

    def testVerifyCreationDifferentHashesSamePassword(self):
        password = "minhasenha123"
        hash1 = self.pm.hashPassword(password)
        new_pm = PasswordManager()
        hash2 = new_pm.hashPassword(password)

        self.assertNotEqual(hash1, hash2)

if __name__ == '__main__':
    unittest.main()