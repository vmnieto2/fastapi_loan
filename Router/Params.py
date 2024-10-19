from Utils.tools import Tools
from fastapi import APIRouter, Request, Depends
from Utils.decorator import http_decorator
from Class.Params import Param
from Middleware.jwt_bearer import JWTBearer

tools = Tools()
param_router = APIRouter()

@param_router.post('/params/get_type_document', tags=["Params"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def get_type_document(request: Request):
    response = Param().get_type_document()
    return response

@param_router.post('/params/get_type_user', tags=["Params"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def get_type_user(request: Request):
    response = Param().get_type_user()
    return response

@param_router.post('/params/delete_param', tags=["Params"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def delete_param(request: Request):
    data = getattr(request.state, "json_data", {})
    response = Param().delete_param(data)
    return response

@param_router.post('/params/update_param', tags=["Params"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def update_param(request: Request):
    data = getattr(request.state, "json_data", {})
    response = Param().update_param(data)
    return response

@param_router.post('/params/create_param', tags=["Params"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def create_param(request: Request):
    data = getattr(request.state, "json_data", {})
    response = Param().create_param(data)
    return response
