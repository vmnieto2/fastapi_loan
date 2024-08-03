from Utils.tools import Tools
from fastapi import APIRouter, Request
from Utils.decorator import http_decorator
from Class.User import User

tools = Tools()
user_router = APIRouter()

@user_router.post('/login', tags=["Auth"])
@http_decorator
def login(request: Request):
    data = getattr(request.state, "json_data", {})
    response = User().login(data)
    return response
