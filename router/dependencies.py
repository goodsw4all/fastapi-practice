from fastapi import APIRouter, Depends, Request


def log_func_dependency(mesg: str):
    return "[LOG]" + mesg


router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies'],
    dependencies=[Depends(log_func_dependency)]
)


def convert_params(request: Request, seperator: str):
    query = []
    for key, value in request.query_params.items():
        query.append(f"{key} {seperator} {value}")

    return query


def convert_headers(request: Request, seperator: str = '-11-', query=Depends(convert_params)):
    out_headers = []

    for key, valu in request.headers.items():
        out_headers.append(f"{key} {seperator} {valu}")

    return {
        'headers': out_headers,
        'query': query
    }


@router.get('')
def get_items(qparam: str, seperator: str = '-0-', headers=Depends(convert_headers)):
    return {
        'items': ['a', 'b', 'c'],
        'headers': headers
    }


@router.post('')
def create_items(headers=Depends(convert_headers)):
    return {
        'result': 'item created',
        'headers': headers
    }


class Account:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


@router.get('/user')
def create_user(name: str, email: str, password: str,
                account: Account = Depends()):
    return {
        'name': account.name,
        'email': account.email,
    }
