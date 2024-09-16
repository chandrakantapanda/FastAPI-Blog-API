from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    name: str
    email: EmailStr  

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/users/",status_code=status.HTTP_201_CREATED)
def create_user(user:UserBase, db:db_dependency):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user = models.User(**user.dict()) #unpacking the dictionary
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        # logger.info("User creation failed due to missing commit")
        # raise HTTPException(status_code=500, detail="Failed to save user data")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id:int, db:db_dependency):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_post(post:PostBase, db:db_dependency):
    try:
        db_post = models.Post(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@app.get("/posts{post_id}",status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: db_dependency):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(post)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")   
    
    