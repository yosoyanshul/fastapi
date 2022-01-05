from os import stat
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import session
from starlette import status
from ..database import get_db
from .. import models, oauth2, schemas 

router = APIRouter(prefix= "/vote", tags = ["voting"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def likeManagement(payload: schemas.LikeInput, db:session = Depends(get_db), 
user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == payload.post_id, models.Vote.user_id == user.id)
    print(user.id)
    if payload.vote_dir == 1:
        if not vote_query.first():
            like = models.Vote(post_id = payload.post_id, user_id = user.id)
            db.add(like)
            db.commit()
            db.refresh(like)
            return like
        return "already voted"
    else:
        if vote_query.first():
            vote_query.delete(synchronize_session = False)
            db.commit()
            return {"status":status.HTTP_204_NO_CONTENT}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post unavailable")



