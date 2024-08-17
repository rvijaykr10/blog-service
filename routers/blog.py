from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from models import Blog
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix='/blog', tags=['blog'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class BlogRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=300)
    author: str = Field(min_length=1)
    rating: int = Field(gt=0, lt=6)
    
    model_config = {
        "json_schema_extra": {
            "example" : {
                "title" : "Learn FastAPI",
                "description" : "Become FastAPI expert",
                "author" : "John Doe",
                "rating": 4
            }
        }
    }

@router.get("", status_code=status.HTTP_200_OK)
async def get_blogs(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Blog).filter(Blog.owner_id == user.get('id')).all()

@router.get("/{blog_id}", status_code=status.HTTP_200_OK)
async def get_blog(user: user_dependency, db: db_dependency, blog_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    blog_model = db.query(Blog).filter(Blog.id == blog_id).filter(Blog.owner_id == user.get('id')).first()
    if blog_model is not None:
        return blog_model
    raise HTTPException(status_code=404, detail='Blog not found.')

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(user: user_dependency, db: db_dependency, blog_request:BlogRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    blog_model = Blog(**blog_request.model_dump(), owner_id=user.get('id'))
    db.add(blog_model)
    db.commit()

@router.put("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(user: user_dependency, db: db_dependency, blog_request:BlogRequest, blog_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    blog_model = db.query(Blog).filter(Blog.id == blog_id).filter(Blog.owner_id == user.get('id')).first()
    if blog_model is None:
        raise HTTPException(status_code=404, detail='Blog not found.')

    blog_model.title = blog_request.title
    blog_model.description = blog_request.description
    blog_model.author = blog_request.author
    blog_model.rating = blog_request.rating

    db.add(blog_model)
    db.commit()

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(user: user_dependency, db: db_dependency, blog_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    blog_model = db.query(Blog).filter(Blog.id == blog_id).filter(Blog.owner_id == user.get('id')).first()
    if blog_model is None:
        raise HTTPException(status_code=404, detail='Blog not found.')
    
    db.query(Blog).filter(Blog.id == blog_id).filter(Blog.owner_id == user.get('id')).delete()
    db.commit()
        