from fastapi import FastAPI, Response, status

from router import blog_get
from router import blog_post

app = FastAPI()
app.include_router(blog_get.router)  # Modulization
app.include_router(blog_post.router)


@app.get('/hello')
def index():  # Name doesn't matter, but not good for code reading
    return {'message': 'Hello, world'}
