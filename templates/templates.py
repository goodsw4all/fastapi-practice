from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from schemas import ProductBase

router = APIRouter(
    prefix='/templates',
    tags=['templates']
)

templates = Jinja2Templates(directory="templates")


@router.get("/products/{id}", response_class=HTMLResponse)
def get_products(id: str, request: Request):
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "id": id,
        })


@router.post("/products/{id}", response_class=HTMLResponse)
def get_products(id: str,
                 product: ProductBase,
                 request: Request,
                 bt: BackgroundTasks
                 ):
    bt.add_task(log_template_call, f'Templates BackgroundTasks {id}')
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "id": id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
        })


def log_template_call(message: str):
    print(f'{message}')
