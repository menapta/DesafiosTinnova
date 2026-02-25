# import unittest
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from app.PasswordManager import PasswordManager
# from app.repository.LoginRepository import LoginRepository

# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# class TestLoginRepository(unittest.TestCase):
#     def setUp(self):
#         with engine.connect() as conn:
#             conn.execute(text("""
#                 CREATE TABLE users (
#                     uuid TEXT PRIMARY KEY,
#                     username TEXT,
#                     typeuser TEXT,
#                     passwordcrypt TEXT
#                 )
#             """))
#             conn.commit()
        
#         self.db_session = TestingSessionLocal()
#         self.pm = PasswordManager()

#     def tearDown(self):
#         self.db_session.close()

#         with engine.connect() as conn:
#             conn.execute(text("DROP TABLE users"))
#             conn.commit()

#     def testGetUserByUsernameSuccess(self):
#         senha_plana = "senha_correta"
#         hash_real = self.pm.hashPassword(senha_plana)
        
#         self.db_session.execute(text("""
#             INSERT INTO users (uuid, username, typeuser, passwordcrypt) 
#             VALUES ('123', 'zecaurubu', 'admin', :hash)
#         """), {"hash": hash_real})
#         self.db_session.commit()

#         repo = LoginRepository(self.db_session)
#         user = repo.getUserByUsername("zecaurubu", senha_plana)

#         self.assertIsNotNone(user)
#         self.assertEqual(user["username"], "zecaurubu")
#         self.assertEqual(user["typeuser"], "admin")

#     def testGetUserNotFound(self):
#         repo = LoginRepository(self.db_session)
#         user = repo.getUserByUsername("inexistente", "qualquer_senha")
#         self.assertIsNone(user)


import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.repositories.LoginRepository import LoginRepository
from app.PasswordManager import PasswordManager
from app.Logger import Logger
from app.userDB import userDB
logger = Logger.createLogger(__name__)

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/db_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class LoginRepositoriyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    uuid TEXT PRIMARY KEY,
                    username TEXT,
                    typeuser TEXT,
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
            INSERT INTO users (uuid, username, typeuser, passwordcrypt) 
            VALUES ('uuid-test-123', 'matheus_test', 'admin', :pw)
        """), {"pw": hashed_pw})
        self.db_session.commit()


        repo = LoginRepository(self.db_session)
        user: userDB | None = repo.getUserByUsername("matheus_test", password)


        self.assertIsNotNone(user)
        self.assertEqual(user.username, "matheus_test")
        self.assertEqual(user.typeuser, "admin")

    def test_get_user_invalid_password(self):
        hashed_pw = self.pm.hashPassword("senha_correta")
        self.db_session.execute(text("""
            INSERT INTO users (uuid, username, typeuser, passwordcrypt) 
            VALUES ('uuid-test-456', 'matheus_test', 'admin', :pw)
        """), {"pw": hashed_pw})
        self.db_session.commit()

        repo = LoginRepository(self.db_session)
        user = repo.getUserByUsername("matheus_test", "SENHA_ERRADA")

        self.assertIsNone(user)