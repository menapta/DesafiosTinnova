from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..models.userDB import userDB


from ..DBConn import getDB
from ..services.LoginService import LoginService
from ..repositories.LoginRepository import LoginRepository
from .. import Logger


SECRET_KEY = "alongsecretkeythatshouldbereplacedwithenvvariable"

logger = Logger.createLogger(__name__)
router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str



@router.post("/login")
def login(userData: LoginRequest, db: Session = Depends(getDB)):
    
    logger.info(f"Attempting login for user: {userData.username}")

    repository = LoginRepository(db)
    service = LoginService(repository)
    
    # if userData.username == None or userData.password == None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Fields 'userName' and 'password' are required!"
    #     )
    
    
    user: userDB | None = service.login(userData.username, userData.password)

    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorized !"
        )
    logger.debug(f"Repository for user: {user.username}")
        
    token = jwt.encode(
        {"user": user.username,"type": user.usertype, "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"token": token}
