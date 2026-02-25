
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..Logger import Logger
from ..PasswordManager import PasswordManager
from ..userDB import userDB

logger = Logger.createLogger(__name__)
class LoginRepository:
    def __init__(self, db_session: Session):
        self.repository: LoginRepository = self
        self.db = db_session

    def getUserByUsername(self, username: str, password: str) -> userDB | None:

        logger.info(f"Fetching user with username: {username}")
        print(f"Fetching user with username: {username}")
        
        query = text("SELECT uuid, username, typeuser, passwordcrypt FROM users WHERE username = :u")
        result = self.db.execute(query, {"u": username}).fetchone()

        if result is None:
            logger.debug(f"No user found with username: {username}")
            return None

        isValidPassword = PasswordManager().verifyPassword(password, result[3])
        
        if not isValidPassword:
            logger.debug(f"Invalid password for user: {username}")
            return None

        user = userDB(
            uuid=str(result[0]),
            username=result[1],
            typeuser=result[2],
        )

        logger.debug(f"User found: {user.username}, type: {user.typeuser}")
        return user