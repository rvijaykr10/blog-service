from fastapi import FastAPI, Body

app = FastAPI()

BLOGS = [
    {'blog_id': 1, 'blog_title': 'blog name 1', 'blog_author': 'author 1'},
    {'blog_id': 2, 'blog_title': 'blog name 2', 'blog_author': 'author 2'},
    {'blog_id': 3, 'blog_title': 'blog name 3', 'blog_author': 'author 3'},
    {'blog_id': 4, 'blog_title': 'blog name 4', 'blog_author': 'author 2'},
    {'blog_id': 5, 'blog_title': 'blog name 5', 'blog_author': 'author 3'},
    ]

# GET APIs
@app.get('/blogs')
async def blog_posts():
    return BLOGS

@app.get('/blogs/')
async def blog_posts_by_title(blog_title:str):
    for blog in BLOGS:
        if blog.get('blog_title').casefold() == blog_title.casefold():
            return blog

@app.get('/blogs/{blog_title}')
async def blog_posts_by_title(blog_title:str):
    for blog in BLOGS:
        if blog.get('blog_title').casefold() == blog_title.casefold():
            return blog

@app.get('/blogs/{blog_title}/')
async def blog_posts_by_title_and_author(blog_title:str, blog_author:str):
    for blog in BLOGS:
        if blog.get('blog_title').casefold() == blog_title.casefold() \
            and blog.get('blog_author').casefold() == blog_author.casefold():
            return blog

# POST APIs       
@app.post('/blogs/create_blog')
async def create_blog_post(new_blog_post=Body()):
    BLOGS.append(new_blog_post)

# PUT APIs
@app.put('/blogs/update_blog')
async def update_blog_post(updated_blog_post=Body()):
    for i in range(len(BLOGS)):
        if BLOGS[i].get('blog_id').casefold() == updated_blog_post.get('blog_id').casefold():
            BLOGS[i] = updated_blog_post