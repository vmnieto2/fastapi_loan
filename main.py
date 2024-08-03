from fastapi import FastAPI
from Config.db import BASE, engine
from Middleware.get_json import JSONMiddleware
from Router.User import user_router
from Router.Params import param_router
from Router.Client import client_router
from Router.Loan import loan_router
from Router.Payment import payment_router

app = FastAPI()
app.title = "Loan Project"
app.version = "0.0.1"
app.add_middleware(JSONMiddleware)
app.include_router(user_router)
app.include_router(param_router)
app.include_router(client_router)
app.include_router(loan_router)
app.include_router(payment_router)

BASE.metadata.create_all(bind=engine)

