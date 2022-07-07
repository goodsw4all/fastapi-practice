from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get('/hello')
def index():  # Name doesn't matter, but not good for code reading
    return {'message': 'Hello, world'}


@app.get('/blog/all')
def index(page=1, page_size: Optional[int] = None):
    return {'message': f'All {page_size} blogs on page {page}'}


@app.get('/blog/{id}/comments/{comment_id}')
def index(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


@app.get('/blog/type/{type}')
def index(type: BlogType):
    return {'message': f'{type}'}


@app.get('/blog/{id}')
def index(id: int):  # pydantic for type validation
    return {'message': f'{id}'}
