from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api import api_router
from templates import templates_router


app = FastAPI()
app.mount('/scripts', app=StaticFiles(directory='scripts'), name='scripts')
app.include_router(api_router)
app.include_router(templates_router)
