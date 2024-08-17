from fastapi import FastAPI
import models
from database import engine
from routers import auth, blog

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(blog.router)