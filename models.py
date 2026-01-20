from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)


class Game(Base):
    __tablename__ = "Games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    style = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")

