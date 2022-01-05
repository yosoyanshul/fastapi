from base64 import decode
from fastapi.param_functions import Depends, Header
from jose import JWTError, jwt
from datetime import date, datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from sqlalchemy.sql.functions import mode
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response 
from . import database, models


from app import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def generate_token(body: dict):
    to_encode = body.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_token(token:str, credential_exception):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = decoded.get("id")

        if id is None:
            raise credential_exception
    
        token_data = schemas.TokenData(id=id)
        
    except JWTError:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db : session = Depends(database.get_db)):
    credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
    )

    token = verify_token(token, credential_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user


