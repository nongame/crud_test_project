from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import List
from sqlalchemy.orm import Session

from models import Base, User, Game
from database import engine, session_local
from schemas import UserCreate, User as DbUser, GameResponse, GameCreate, GameUpdate


app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=DbUser)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/games/", response_model=GameResponse)
async def create_game(
    game: GameCreate,
    db: Session = Depends(get_db)) -> GameResponse:
    db_user = db.query(User).filter(User.id == game.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_game = Game(name=game.name, style=game.style, author_id=game.author_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game

@app.get("/games/", response_model=List[GameResponse])
async def get_games(db: Session = Depends(get_db)) -> List[GameResponse]:
    return db.query(Game).all()

@app.patch("/games/{game_id}", response_model=GameResponse)
async def patch_game(
    game_id: int = Path(..., gt=0),
    game_patch: GameUpdate = Body(...),
    db: Session = Depends(get_db)) -> GameResponse:
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    if game_patch.name is not None:
        db_game.name = game_patch.name

    if game_patch.style is not None:
        db_game.style = game_patch.style

    if game_patch.author_id is not None:
        db_user = db.query(User).filter(User.id == game_patch.author_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db_game.author_id = game_patch.author_id

    db.commit()
    db.refresh(db_game)
    return db_game


@app.delete("/games/{game_id}", status_code=204)
async def delete_game(
    game_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(db_game)
    db.commit()