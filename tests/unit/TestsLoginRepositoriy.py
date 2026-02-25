
import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.repositories.LoginRepository import LoginRepository
from app.PasswordManager import PasswordManager
from app import Logger
from app.models.userDB import userDB
logger = Logger.createLogger(__name__)

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestsLoginRepositoriy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    uuid TEXT PRIMARY KEY,
                    username TEXT,
                    usertype TEXT,
                    passwordcrypt TEXT
                )
            """))
            conn.commit()

    def setUp(self):
        self.db_session = TestingSessionLocal()
        self.pm = PasswordManager()
        
        self.db_session.execute(text("DELETE FROM users"))
        self.db_session.commit()

    def tearDown(self):
        self.db_session.close()

    def test_get_user_by_username_success(self):
        logger.info("Starting test_get_user_by_username_success")
        password = "minha_senha_123"
        hashed_pw = self.pm.hashPassword(password)
        
        self.db_session.execute(text("""
            INSERT INTO users (uuid, username, usertype, passwordcrypt) 
            VALUES ('uuid-test-123', 'matheus_test', 'admin', :pw)
        """), {"pw": hashed_pw})
        self.db_session.commit()


        repo = LoginRepository(self.db_session)
        user: userDB | None = repo.getUserByUsername("matheus_test", password)


        self.assertIsNotNone(user)
        self.assertEqual(user.username, "matheus_test")
        self.assertEqual(user.usertype, "admin")

    def test_get_user_invalid_password(self):
        hashed_pw = self.pm.hashPassword("senha_correta")
        self.db_session.execute(text("""
            INSERT INTO users (uuid, username, usertype, passwordcrypt) 
            VALUES ('uuid-test-456', 'matheus_test', 'admin', :pw)
        """), {"pw": hashed_pw})
        self.db_session.commit()

        repo = LoginRepository(self.db_session)
        user = repo.getUserByUsername("matheus_test", "SENHA_ERRADA")

        self.assertIsNone(user)