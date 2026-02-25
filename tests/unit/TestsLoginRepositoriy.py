
import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.repositories.LoginRepository import LoginRepository
from app.PasswordManager import PasswordManager
from app import Logger
from app.models.userDB import userDB
from pathlib import Path

logger = Logger.createLogger(__name__)

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

current_file = Path(__file__).resolve()
root_dir = current_file.parents[2]
sql_path = root_dir / "init-scripts" / "0createUsersTable.sql"

class TestsLoginRepositoriy(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     with engine.connect() as conn:
    #         conn.execute(text("""
    #             CREATE TABLE IF NOT EXISTS users (
    #                 uuid TEXT PRIMARY KEY,
    #                 username TEXT,
    #                 usertype TEXT,
    #                 passwordcrypt TEXT
    #             )
    #         """))
    #         conn.commit()
    @classmethod
    def setUpClass(cls):
        with open(sql_path, "r") as f:
            sql_script = f.read()

        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(sql_script))
        logger.info(f"Database schema synchronized from SQL file. {sql_path}")

    def setUp(self):
        self.dbSession = TestingSessionLocal()
        self.pm = PasswordManager()
        
        self.dbSession.execute(text("DELETE FROM users"))
        self.dbSession.commit()

    def tearDown(self):
        self.dbSession.close()

    def testSuccessGetUserByUsername(self):
        logger.info("Starting test_get_user_by_username_success")
        password = "minha_senha_123"
        hashed_pw = self.pm.hashPassword(password)
        
        self.dbSession.execute(text("""
            INSERT INTO users (uuid, username, usertype, passwordcrypt) 
            VALUES ('uuid-test-123', 'matheus_test', 'admin', :pw)
        """), {"pw": hashed_pw})
        self.dbSession.commit()


        repo = LoginRepository(self.dbSession)
        user: userDB | None = repo.getUserByUsername("matheus_test", password)


        self.assertIsNotNone(user)
        self.assertEqual(user.username, "matheus_test")
        self.assertEqual(user.usertype, "admin")

    def testgetUSerInvalidPassword(self):
        hashedPAssword = self.pm.hashPassword("senha_correta")
        self.dbSession.execute(text("""
            INSERT INTO users (uuid, username, usertype, passwordcrypt) 
            VALUES ('uuid-test-456', 'matheus_test', 'admin', :pw)
        """), {"pw": hashedPAssword})
        self.dbSession.commit()

        repo = LoginRepository(self.dbSession)
        user = repo.getUserByUsername("matheus_test", "SENHA_ERRADA")

        self.assertIsNone(user)