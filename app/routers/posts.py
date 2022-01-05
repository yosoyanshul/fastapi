from typing import List, Optional
from pydantic.networks import PostgresDsn
from sqlalchemy.orm import session
from .. import schemas, models, oauth2
from ..database import get_db
from fastapi import Depends, HTTPException, status, Response, APIRouter

router = APIRouter(prefix="/posts", tags=['posts'])

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: session = Depends(get_db), 
user: int = Depends(oauth2.get_current_user), limit: int = 10, skip : int = 0, search : Optional[str] = ""):

    post = db.query(models.Posts).filter(models.Posts.content.contains(search)).limit(limit).offset(skip).all()

    return post

@router.post("/",response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: session = Depends(get_db), 
user: int = Depends(oauth2.get_current_user)):
    temp = post.dict()
    temp['owner_id'] = user.id
    new_post = models.Posts(**temp)
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_one_post(id:int, db: session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    req_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if req_post:
        return req_post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


@router.delete("/{id}")
def delete_post(id:int, db: session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post:
        if post.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="fuck off")
        post_query.delete(synchronize_session = False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "post not present")

@router.put("/{id}")
def update_post(id: int, post: schemas.PostBase, db: session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    changes_post = db.query(models.Posts).filter(models.Posts.id == id)
    freq = post.dict()
    freq["id"] = id
    if changes_post.first():
        changes_post.update(freq, synchronize_session = False )
        db.commit()
        return {"message":Response(status_code=status.HTTP_202_ACCEPTED), "status":freq}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)