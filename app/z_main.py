from typing import Union

from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body

from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

# db: Session = Depends(get_db)
app = FastAPI()

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host="localhost", dbname="fastapi", user="postgres", password=1234, cursor_factory=RealDictCursor)

        # Open a cursor to perform database operations
        cur = conn.cursor()

        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)

        # Wait 2 seconds until next retry
        time.sleep(2)

Pydantic form validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts where id = %s""", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # print(post)
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int):
    cur.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return {"data": deleted_post}
    

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cur.execute("""UPDATE posts SET title = %s,  content = %s, published = %s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    updated_post = cur.fetchone()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return {"data": updated_post}