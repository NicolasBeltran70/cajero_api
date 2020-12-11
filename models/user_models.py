from pydantic import BaseModel 

#creamos clases por cada estado  por el que pasara el usuario
class UserIn(BaseModel): 
    username: str
    password: str

class UserOut(BaseModel): 
    username: str
    balance: int
