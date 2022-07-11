from typing import Optional
from fastapi import FastAPI, Response, status
from enum import Enum

app = FastAPI()


@app.get('/hello')
def index():  # Name doesn't matter, but not good for code reading
    return {'message': 'Hello, world'}


@app.get('/blog/all',
         tags=['blog'],
         summary='Retrieve all blogs',
         description='This api is fetching all blogs',
         response_description='list of blogs'
         )
def index(page=1, page_size: Optional[int] = None):
    return {'message': f'All {page_size} blogs on page {page}'}


@app.get('/blog/{id}/comments/{comment_id}', tags=['blog', 'comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """
    Simulates retriving a comment of a blog
    - **id** : mandatory argument
    """

    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


@app.get('/blog/type/{type}', tags=['blog'])
def index(type: BlogType):
    return {'message': f'{type}'}


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, tags=['blog'])
def index(id: int, response: Response):  # pydantic for type validation
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'err': 'not found'}
    return {'message': f'{id}'}
