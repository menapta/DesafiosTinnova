from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
import jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator, model_validator

from ..models.UserDB import UserDB


from ..DBConn import getDB
from ..services.LoginService import LoginService
from ..repositories.LoginRepository import LoginRepository
from .. import Logger
from ..RateLimiter import limiter

SECRET_KEY = "alongsecretkeythatshouldbereplacedwithenvvariable"

logger = Logger.createLogger(__name__)
router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode="after")
    def verifyUsernameAndPassword(self):
        if not self.username  or not self.password:
            raise ValueError("")
        return self


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, userData: LoginRequest, db: Session = Depends(getDB)):
    
    logger.info(f"Attempting login for user: {userData.username}")

    repository = LoginRepository(db)
    service = LoginService(repository)
    

    user: UserDB | None = service.login(userData.username, userData.password)

    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized !"
        )
    logger.debug(f"Repository for user: {user.username}")
        
    token = jwt.encode(
        {"user": user.username,"type": user.usertype, "exp": datetime.utcnow() + timedelta(minutes=4320)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"token": token}
