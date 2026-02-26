from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import Logger
from ..PasswordManager import PasswordManager
from ..models.UserDB import UserDB

logger = Logger.createLogger(__name__)
class LoginRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def getUserByUsername(self, username: str, password: str) -> UserDB | None:

        logger.info(f"Fetching user with username: {username}")
        print(f"Fetching user with username: {username}")
        
        query = text("SELECT uuid, username, usertype, passwordcrypt FROM users WHERE username = :u")
        result = self.db.execute(query, {"u": username}).fetchone()

        if result is None:
            logger.debug(f"No user found with username: {username}")
            return None

        isValidPassword = PasswordManager().verifyPassword(password, result[3])
        
        if not isValidPassword:
            logger.debug(f"Invalid password for user: {username}")
            return None

        user = UserDB(
            uuid=str(result[0]),
            username=result[1],
            usertype=result[2],
        )

        logger.debug(f"User found: {user.username}, type: {user.usertype}")
        return user