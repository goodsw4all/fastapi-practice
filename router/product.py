import time


from typing import List, Optional
from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['watch', 'camera', 'phone']


async def time_consuming_function():
    time.sleep(5)
    return 'ok'


@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get('/all')
async def get_all_product():
    await time_consuming_function()
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key='test_cookie', value="test_cookie_value")
    return response


@router.get('/withheader')
def get_products(
        response: Response,
        custom_headers: Optional[List[str]] = Header(None),
        test_cookie: Optional[str] = Cookie(None)
):
    if custom_headers:
        response.headers['custom_response_headers'] = " , ".join(
            custom_headers)

    print(response.headers['custom_response_headers'])
    return {
        "data": products,
        "custom_header": custom_headers,
        "my_cookie": test_cookie
    }


@router.get('/{id}', responses={
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>",
            }
        },
        "description": "Returns the HTML for an object"
    },
    404: {
        "content": {
            "text/plain": {
                "example": "Product not available",
            }
        },
        "description": "A cleartext error message"
    }
})
def get_product(id: int):
    if id >= len(products):
        out = "Product not available"
        return PlainTextResponse(status_code=404, content=out, media_type="text/plain")

    product = products[id]
    out = f"""
    <head>
        <style>
        .product {{
            width: 500px;
            hegith: 30px;
            border: 2px inset green;
            background-color: lightblue;
            text-align: center;
        }}
        </style>
    </head>
    <div class="product">{id}</div>
    """
    # return Response(content=out, media_type="text/html")
    return HTMLResponse(content=out)
