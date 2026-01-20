from pydantic import BaseModel, ConfigDict

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
