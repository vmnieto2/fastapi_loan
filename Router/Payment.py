from Utils.tools import Tools
from fastapi import APIRouter, Request, Depends
from Utils.decorator import http_decorator
from Class.Payment import Payment
from Middleware.jwt_bearer import JWTBearer
from Schemas.payment import Payment as PaymentSchema

tools = Tools()
payment_router = APIRouter()


@payment_router.post('/payment/create_payment', tags=["Payment"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def create_payment(request: Request, payment: PaymentSchema):
    data = getattr(request.state, "json_data", {})
    response = Payment().create_payment(data)
    return response

@payment_router.post('/payment/show_payments', tags=["Payment"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def show_payments(request: Request):
    data = getattr(request.state, "json_data", {})
    response = Payment().show_payments(data)
    return response
