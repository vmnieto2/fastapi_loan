from Utils.tools import Tools
from fastapi import APIRouter, Request, Depends
from Utils.decorator import http_decorator
from Class.Loan import Loan
from Middleware.jwt_bearer import JWTBearer
from Schemas.loan import Loan as LoanSchema

tools = Tools()
loan_router = APIRouter()


@loan_router.post('/loan/create_loan', tags=["Loan"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def create_loan(request: Request, loan: LoanSchema):
    data = getattr(request.state, "json_data", {})
    response = Loan().create_loan(data)
    return response

@loan_router.post('/loan/show_loans_by_client', tags=["Loan"], response_model=dict, dependencies=[Depends(JWTBearer())])
@http_decorator
def show_loans_by_client(request: Request):
    data = getattr(request.state, "json_data", {})
    response = Loan().show_loans_by_client(data)
    return response
