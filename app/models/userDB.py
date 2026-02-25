from pydantic import BaseModel


class UserDB(BaseModel):
    uuid: str
    username: str
    usertype: str