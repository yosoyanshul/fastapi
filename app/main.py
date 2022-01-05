from os import name
from fastapi import FastAPI,status, Depends
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import session
from starlette.responses import Response
from time import sleep
from .database import get_db, engine
from . import models
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####### db connectivity normal way
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database = 'fastapi', user = 'postgres', password = 'abc', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('\ndatabase connection was successful !!!')
        break
    except Exception as error:
        print('database connection Failed')
        print('Error is :', error)
        sleep(2) 


#post validator
class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class User(BaseModel):
    name:str
    address:str
    tnc:bool = True


@app.get("/")
def root():
    return {"message": "Hello Moto"}



###########SHOW ALL POSTS


@app.get("/posts")
def getPost():
    # cursor.execute("""SELECT * FROM posts""")
    # my_post = cursor.fetchall()
    my_post = db.query(models.Posts).all()
    return {'Data':my_post}

##########CREATE A POST

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createPost(post: Post): #post is a validating class derived form base model

    cursor.execute("""INSERT INTO posts (title, content, published ) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data':new_post}



####################    GET A POST


@app.get("/posts/{id}")
def get_a_post(id: int):
    
    cursor.execute(f"""SELECT * FROM posts WHERE id = {str(id)}""")
    req_post = cursor.fetchone()

    if req_post: 
        return f"Data: {req_post}"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post you are trying to get doesn't exist")


##########      DELETE A POST


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    cursor.execute(f"""DELETE FROM posts WHERE id = {str(id)} returning *""")
    del_post = cursor.fetchone()
    conn.commit()
    if del_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post you want to delete doesn't exist")


##############        UPDATE A POST


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s returning *""",(post.title, post.content, post.published, str(id)))
    up_post = cursor.fetchone()
    conn.commit()
    if up_post:
        return f'Success: {up_post}'
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exists")




@app.get("/user")
def get_users(db: session = Depends(get_db)):
    users = db.query(models.Users).all()
    return {f"users are:":users}

@app.post('/user')
def create_user(user:User, db: session = Depends(get_db)):
    models.Users(name=user.name, address=user.address, tnc = user.tnc)
    
    
