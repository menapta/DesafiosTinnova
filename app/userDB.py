from pydantic import BaseModel


class userDB(BaseModel):
    uuid: str
    username: str
    typeuser: str