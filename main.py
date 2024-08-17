from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Blog:
    blog_id: int
    blog_title: str
    blog_author: str
    blog_rating: str
    
    def __init__(self, blog_id, blog_title, blog_author, blog_rating):
        self.blog_id=blog_id
        self.blog_title=blog_title
        self.blog_author=blog_author
        self.blog_rating=blog_rating
    
class BlogRequest(BaseModel):
    blog_id: Optional[int] = None
    blog_title: str = Field(min_length=1)
    blog_author: str = Field(min_length=1)
    blog_rating: int = Field(gt=0, lt=6)
    
    model_config = {
        "json_schema_extra": {
            "example" : {
                "blog_id" : 1,
                "blog_title" : "Learn FastAPI",
                "blog_author" : "John Doe",
                "blog_rating": 4
            }
        }
    }

BLOGS = [
    Blog(1, 'blog name 1', 'author 1', 4),
    Blog(2, 'blog name 2', 'author 2', 3),
    Blog(3, 'blog name 3', 'author 3', 5),
    Blog(4, 'blog name 4', 'author 4', 2),
    Blog(5, 'blog name 5', 'author 5', 2),
    Blog(6, 'blog name 6', 'author 6', 4),
]

# GET APIs
@app.get('/blogs', status_code=status.HTTP_200_OK)
async def get_blog_posts():
    return BLOGS

@app.get('/blogs/{blog_id}', status_code=status.HTTP_200_OK)
async def get_blog_post(blog_id:int = Path(gt=0)):
    for blog in BLOGS:
        if blog.blog_id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail='Item not found')
        
@app.get('/blogs/', status_code=status.HTTP_200_OK)
async def get_blog_post_by_rating(blog_rating: int=Query(gt=0, lt=6)):
    blogs_to_return = []
    for blog in BLOGS:
        if blog.blog_rating == blog_rating:
            blogs_to_return.append(blog)
    return blogs_to_return

# @app.get('/blogs/')
# async def blog_posts_by_title(blog_title:str):
#     for blog in BLOGS:
#         if blog.get('blog_title').casefold() == blog_title.casefold():
#             return blog

# @app.get('/blogs/{blog_title}')
# async def blog_posts_by_title(blog_title:str):
#     for blog in BLOGS:
#         if blog.get('blog_title').casefold() == blog_title.casefold():
#             return blog

# @app.get('/blogs/{blog_title}/')
# async def blog_posts_by_title_and_author(blog_title:str, blog_author:str):
#     for blog in BLOGS:
#         if blog.get('blog_title').casefold() == blog_title.casefold() \
#             and blog.get('blog_author').casefold() == blog_author.casefold():
#             return blog

# POST APIs       
@app.post('/blogs/create_blog', status_code=status.HTTP_201_CREATED)
async def create_blog_post(new_blog_post:BlogRequest):
    new_blog = Blog(**new_blog_post.model_dump())
    BLOGS.append(new_blog)

# PUT APIs
@app.put('/blogs/update_blog', status_code=status.HTTP_204_NO_CONTENT)
async def update_blog_post(updated_blog_post:BlogRequest):
    blog_changed = False
    for i in range(len(BLOGS)):
        # if BLOGS[i].get('blog_id') == updated_blog_post.get('blog_id'):   # bcoz it is python dict
        if BLOGS[i].blog_id == updated_blog_post.blog_id:                   # bcoz it is python object
            BLOGS[i] = updated_blog_post
            blog_changed = True
    if not blog_changed:
        raise HTTPException(status_code=404, detail='Item not found')
            
# DELETE APIs
@app.delete('/blogs/delete_blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(blog_id:int=Path(gt=0)):
    blog_changed = False
    for i in range(len(BLOGS)):
        # if BLOGS[i].get('blog_id') == blog_id: # bcoz it is python dict
        if BLOGS[i].blog_id == blog_id:          # bcoz it is python object
            BLOGS.pop(i)
            blog_changed = True
            break
    if not blog_changed:
        raise HTTPException(status_code=404, detail='Item not found')