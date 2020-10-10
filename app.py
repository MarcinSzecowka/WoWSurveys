from fastapi import FastAPI
from api import api_router
from templates import templates_router

app = FastAPI()
app.include_router(api_router)
app.include_router(templates_router)