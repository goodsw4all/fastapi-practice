import time
from xmlrpc import client

from fastapi import FastAPI, WebSocket
from fastapi import Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from exceptions import StoryException

from router import blog_get, blog_post, user, article, product, file
from templates import templates

from auth import authentication
from db.database import engine
from db import models
from client import html


app = FastAPI()
app.mount('/static', StaticFiles(directory='files'), name='files')
app.mount('/templates/static',
          StaticFiles(directory='templates/static'), name='static')

# Register the routers
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(templates.router)


# Just fo test end-point in file
# @app.get('/')
# def index():
#     return {'message': 'Hello world!'}


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )


@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)

# @app.exception_handler(HTTPException)
# def story_exception_handler(request: Request, exc: HTTPException):
#     return PlainTextResponse(str(exc), status_code=400)

models.Base.metadata.create_all(engine)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['Duration'] = str(duration)
    return response


origins = [
    'htpp://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
