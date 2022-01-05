from fastapi import Depends, HTTPException, status, Response, APIRouter
from typing import List
from sqlalchemy.orm import session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(prefix="/users",tags = ["users"])

@router.post("/", response_model=schemas.PostUser)
def create_user(body: schemas.CreateUser, db: session = Depends(get_db)):
    user_password = utils.hash(body.password)
    body.password = user_password
    new_user = models.Users(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/", response_model=List[schemas.PostUser])
def get_user(db: session = Depends(get_db)):
    all_user = db.query(models.Users).all()
    return all_user



@router.get("/{id}")
def get_user(id:int, db: session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id)
    if user.first():
        return user.first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{id}")
def del_user(id: int, db: session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id)
    if user.first():
        user.delete(synchronize_session = False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id not found")
