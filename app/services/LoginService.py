from app.repositories import LoginRepository

from ..models.UserDB import UserDB
from .. import Logger


logger = Logger.createLogger(__name__)

class LoginService:

    repository: LoginRepository
    def __init__(self, repository: LoginRepository):
        self.repository: LoginRepository = repository
    
    def login(self, username: str, password: str) -> UserDB | None:
        user: UserDB | None = self.repository.getUserByUsername(username, password)
        logger.debug(f"LoginService: Retrieved user from repository: {user.username if user else 'None'}")

        return user