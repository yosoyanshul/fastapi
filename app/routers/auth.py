from typing import List
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import utils
from .. import schemas, models, oauth2
from ..database import get_db
from fastapi import Depends, HTTPException, status, Response, APIRouter

router = APIRouter(tags=['authentication'])

@router.post("/login", response_model=schemas.Token)
def user_login(credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    
    req_user = db.query(models.Users).filter(models.Users.email ==  credentials.username).first()

    if not req_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify(credentials.password, req_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    token = oauth2.generate_token({"id":req_user.id})

    return {"access_token":token, "token_type":"Bearer"}


    