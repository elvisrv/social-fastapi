from fastapi import APIRouter, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # print(db)
    # print(current_user.id)
    # print(search)

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post).all()

    # print(results)
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    # return {"data": new_post}
    # print(current_user.email)

    # print(**post.dict())
    new_post = models.Post(
        # title=post.title, content=post.content, published=post.published)
        owner_id=current_user.id,
        **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts where id = %s""", (str(id),))
    # post = cur.fetchone()
    # if not post:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            # detail=f"post with id: {id} was not found")
    # print(post)
    # return {"post_detail": post}
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()
    # print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
       
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()

    return post_query.first()