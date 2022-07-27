from pydoc import plainpager
from urllib.request import Request
from exceptions import StoryException
from router import blog_get
from router import blog_post
from router import user
from router import article
from db.database import engine
from db import models
from fastapi import Request, status
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse


app = FastAPI()
app.include_router(user.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get('/hello')
def index():
    return {'message': 'Hello world!'}


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )


# @app.exception_handler(HTTPException)
# def story_exception_handler(request: Request, exc: HTTPException):
#     return PlainTextResponse(str(exc), status_code=400)


models.Base.metadata.create_all(engine)
