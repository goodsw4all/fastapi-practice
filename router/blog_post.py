from email.mime import image
from typing import Optional, List, Dict
from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1', 'v1'}
    image: Image


# Read request body as JSON
# Data validation
@router.post('/new/{id}')  # Path
def create_blog(blog: BlogModel, id: int, version: int = 1):  # Query & Body
    return {
        'id': id,
        'data': blog,
        'version': version
    }


@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel,
                   id: int,
                   comment_id: int = Path(None, gt=5, le=10),
                   comment_title: int = Query(None,
                                              title='Title of the comment',
                                              description='Some description for comment_title',
                                              alias='commentTitle',
                                              #   deprecated=True
                                              ),
                   content: str = Body(...,
                                       min_length=5,
                                       max_length=12,
                                       regex='^[a-z\s]*$'
                                       ),  # Ellipsis, forced
                   v: Optional[List[str]] = Query(['1.0', '1.2']),
                   ):
    return {
        'id': id,
        'data': blog,
        'comment_title': comment_title,
        'content': content,
        'version': v,
        'comment_id': comment_id,
    }
