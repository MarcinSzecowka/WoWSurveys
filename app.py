from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles

from api import api_router
from templates import templates_router, templates

app = FastAPI()
app.mount('/assets', app=StaticFiles(directory='assets'), name='assets')
app.include_router(api_router)
app.include_router(templates_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request})


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_handler(request, _):
    return templates.TemplateResponse("404.html", {"request": request})
