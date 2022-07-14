from typing import Optional
from fastapi import FastAPI, Response, status, APIRouter
from enum import Enum


router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.get('/all',
            summary='Retrieve all blogs',
            description='This api is fetching all blogs',
            response_description='list of blogs'
            )
def index(page=1, page_size: Optional[int] = None):
    return {'message': f'All {page_size} blogs on page {page}'}


@router.get('/{id}/comments/{comment_id}', tags=['comment'])
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


@router.get('/type/{type}')
def index(type: BlogType):
    return {'message': f'{type}'}


@router.get('/{id}', status_code=status.HTTP_200_OK)
def index(id: int, response: Response):  # pydantic for type validation
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'err': 'not found'}
    return {'message': f'{id}'}
