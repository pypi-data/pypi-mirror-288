# modelss/user.py

from pydantic import BaseModel, SecretStr

class User(BaseModel):
    name: str
    username: str
    password: str

class Login(BaseModel):
    username:  str
    password: str
    verification: str
    IV: str
    AES: str

class infoModel(BaseModel):
    info: object