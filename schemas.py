from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    age: int


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass

class GameBase(BaseModel):
    style: str
    name: str
    author_id: int

class GameCreate(GameBase):
    pass

class GameResponse(GameBase):
    id : int
    author : User

    model_config = ConfigDict(from_attributes=True)

class GameUpdate(BaseModel):
    style: Optional[str] = None
    name: Optional[str] = None
    author_id: Optional[int] = None


