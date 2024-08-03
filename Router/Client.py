from Utils.tools import Tools
from fastapi import APIRouter, Request, Depends
from Utils.decorator import http_decorator
from Class.Client import Client
from Middleware.jwt_bearer import JWTBearer
from Schemas.client import Client as ClientSchema

tools = Tools()
client_router = APIRouter()

@client_router.post('/client/save_client', tags=["Client"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def save_client(request: Request, client: ClientSchema):
    data = getattr(request.state, "json_data", {})
    response = Client().save_client(data)
    return response

@client_router.post('/client/get_all_clients', tags=["Client"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def get_all_clients(request: Request):
    response = Client().get_all_clients()
    return response
